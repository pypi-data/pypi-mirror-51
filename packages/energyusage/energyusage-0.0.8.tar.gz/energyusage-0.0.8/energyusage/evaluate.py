import time
import statistics
from timeit import default_timer as timer
from multiprocessing import Process, Queue
import os
import datetime
import subprocess
import queue


import energyusage.utils as utils
import energyusage.convert as convert
import energyusage.locate as locate
import energyusage.report as report

DELAY = .1 # in seconds

def func(user_func, q, *args):
    """ Runs the user's function and puts return value in queue """

    value = user_func(*args)
    q.put(value)

def energy(user_func, *args, powerLoss = 0.8):
    """ Evaluates the kwh needed for your code to run

    Parameters:
       user_func (function): user's function

    Returns:
        (process_kwh, return_value, watt_averages)

    """

    baseline_check_seconds = 5
    files, multiple_cpus = utils.get_files()
    is_nvidia_gpu = utils.valid_gpu()
    is_valid_cpu = utils.valid_cpu()

    # GPU handling if Nvidia
    gpu_baseline =[0]
    gpu_process = [0]
    bash_command = "nvidia-smi -i 0 --format=csv,noheader --query-gpu=power.draw"

    for i in range(int(baseline_check_seconds / DELAY)):
        if is_nvidia_gpu:
            output = subprocess.check_output(['bash','-c', bash_command])
            output = float(output.decode("utf-8")[:-2])
            gpu_baseline.append(output)
        if is_valid_cpu:
            files = utils.measure_files(files, DELAY)
            files = utils.update_files(files)
        else:
            time.sleep(DELAY)
        # Adds the most recent value of GPU; 0 if not Nvidia
        last_reading = utils.get_total(files, multiple_cpus) + gpu_baseline[-1]
        if last_reading >=0:
            utils.log("Baseline wattage", last_reading)
    utils.newline()

    # Running the process and measuring wattage
    q = Queue()
    p = Process(target = func, args = (user_func, q, *args,))

    start = timer()
    p.start()
    small_delay_counter = 0
    return_value = None
    while(p.is_alive()):
        # Checking at a faster rate for quick processes
        if (small_delay_counter > DELAY):
           delay = DELAY / 10
           small_delay_counter+=1
        else:
           delay = DELAY

        if is_nvidia_gpu:
            output = subprocess.check_output(['bash','-c', bash_command])
            output = float(output.decode("utf-8")[:-2])
            gpu_process.append(output)
        if is_valid_cpu:
            files = utils.measure_files(files, delay)
            files = utils.update_files(files, True)
        else:
            time.sleep(delay)
        # Just output, not added
        last_reading = (utils.get_total(files, multiple_cpus) + gpu_process[-1]) / powerLoss
        if last_reading >=0:
            utils.log("Process wattage", last_reading)
       # Getting the return value of the user's function
        try:
            return_value = q.get_nowait()
            break
        except queue.Empty:
            pass
    p.join()
    end = timer()
    for file in files:
        file.process = file.process[1:-1]
        file.baseline = file.baseline[1:-1]
    if is_nvidia_gpu:
        gpu_baseline_average = statistics.mean(gpu_baseline[2:-1])
        gpu_process_average = statistics.mean(gpu_process[2:-1])
    else:
        gpu_baseline_average = 0
        gpu_process_average = 0

    total_time = end-start # seconds
    # Formatting the time nicely
    timedelta = str(datetime.timedelta(seconds=total_time)).split('.')[0]

    files = utils.average_files(files)

    process_average = utils.get_process_average(files, multiple_cpus, gpu_process_average)
    baseline_average = utils.get_baseline_average(files, multiple_cpus, gpu_baseline_average)
    difference_average = process_average - baseline_average
    watt_averages = [baseline_average, process_average, difference_average]

    # Subtracting baseline wattage to get more accurate result
    process_kwh = convert.to_kwh((process_average - baseline_average)*total_time) / powerLoss

    if is_nvidia_gpu:
        gpu_file = file("GPU", "")
        gpu_file.create_gpu(gpu_baseline_average, gpu_process_average)
        files.append(file("GPU", ""))

    # Logging
    utils.log("Final Readings", baseline_average, process_average, difference_average, timedelta)
    return (process_kwh, return_value, watt_averages, files)


def energy_mix(location):
    """ Gets the energy mix information for a specific location

        Parameters:
            location (str): user's location

        Returns:
            breakdown (list): percentages of each energy type
    """

    if (location == "Unknown" or locate.in_US(location)):
        # Default to U.S. average for unknown location
        if location == "Unknown":
            location = "United States"

        data = utils.get_data("data/json/energy-mix-us.json")
        s = data[location]['mix'] # get state
        coal, oil, gas = s['coal'], s['oil'], s['gas']
        nuclear, hydro, biomass, wind, solar, geo, = \
        s['nuclear'], s['hydro'], s['biomass'], s['wind'], \
        s['solar'], s['geothermal']

        low_carbon = sum([nuclear,hydro,biomass,wind,solar,geo])
        breakdown = [coal, oil, gas, low_carbon]

        return breakdown # list of % of each

    else:
        data = utils.get_data('data/json/energy-mix-intl.json')
        c = data[location] # get country
        total, breakdown =  c['total'], [c['coal'], c['petroleum'], \
        c['naturalGas'], c['lowCarbon']]

        # Get percentages
        breakdown = list(map(lambda x: 100*x/total, breakdown))

        return breakdown # list of % of each


def emissions(process_kwh, breakdown, location):
    """ Calculates the CO2 emitted by the program based on the location

        Parameters:
            process_kwh (int): kWhs used by the process
            breakdown (list): energy mix corresponding to user's location
            location (str): location of user

        Returns:
            emission (float): kilograms of CO2 emitted
            state_emission (float): lbs CO2 per MWh

    """

    if process_kwh < 0:
        raise OSError("Process wattage lower than baseline wattage. Do not run other processes"
         " during the evaluation, or try evaluating a more resource-intensive process.")

    utils.log("Energy Data", breakdown, location)
    state_emission = 0

    # Case 1: Unknown location, default to US data
    # Case 2: United States location
    if location == "Unknown" or locate.in_US(location):
        if location == "Unknown":
            location = "United States"
        # US Emissions data is in lbs/Mwh
        data = utils.get_data("data/json/us-emissions.json")
        state_emission = data[location]
        emission = convert.lbs_to_kgs(state_emission*convert.to_MWh(process_kwh))

    # Case 3: International location
    else:
        # Breaking down energy mix
        coal, petroleum, natural_gas, low_carbon = breakdown
        breakdown = [convert.coal_to_carbon(process_kwh * coal/100),
                     convert.petroleum_to_carbon(process_kwh * petroleum/100),
                     convert.natural_gas_to_carbon(process_kwh * natural_gas/100), 0]
        emission = sum(breakdown)

    utils.log("Emissions", emission)
    return (emission, state_emission)

def emissions_comparison(process_kwh):
    """ Calculates emissions in different locations """
	
    intl_data = utils.get_data("data/json/energy-mix-intl.json")
    global_emissions, europe_emissions, us_emissions = [], [], []
    # Handling international
    for country in intl_data:
           c = intl_data[country]
           total, breakdown = c['total'], [c['coal'], c['petroleum'], \
           c['naturalGas'], c['lowCarbon']]
           if isinstance(total, float) and float(total) > 0:
               breakdown = list(map(lambda x: 100*x/total, breakdown))
               coal, petroleum, natural_gas, low_carbon = breakdown
               breakdown = [convert.coal_to_carbon(process_kwh * coal/100),
                    convert.petroleum_to_carbon(process_kwh * petroleum/100),
                    convert.natural_gas_to_carbon(process_kwh * natural_gas/100), 0]
               emission = sum(breakdown)
               if locate.in_Europe(country):
                   europe_emissions.append((country,emission))
               else:
                   global_emissions.append((country,emission))
              
    global_emissions.sort(key=lambda x: x[1])
    europe_emissions.sort(key=lambda x: x[1])
            
    # Handling US
    us_data = utils.get_data("data/json/us-emissions.json")
    for state in us_data:
        if (state != "United States" and state != "_units"):
            emission = convert.lbs_to_kgs(us_data[state]*convert.to_MWh(process_kwh))
            us_emissions.append((state, emission))
    us_emissions.sort(key=lambda x: x[1])
    
    max_global, max_europe, max_us = global_emissions[len(global_emissions)-1], \
        europe_emissions[len(europe_emissions)-1], us_emissions[len(us_emissions)-1]
    median_global, median_europe, median_us = global_emissions[len(global_emissions)//2], \
        europe_emissions[len(europe_emissions)//2], us_emissions[len(us_emissions)//2]
    min_global, min_europe, min_us= global_emissions[0], europe_emissions[0], us_emissions[0]
    utils.log('Emissions Comparison', max_global, median_global, min_global, max_europe, \
              median_europe, min_europe, max_us, median_us, min_us)
 

def evaluate(user_func, *args, pdf=False, powerLoss=0.8, energyOutput=False):
    """ Calculates effective emissions of the function

        Parameters:
            user_func: user inputtted function
            pdf (bool): whether a PDF report should be generated
            powerLoss (float): PSU efficiency rating

    """
    #FIXME: if(utils.valid_cpu() or utils.valid_gpu()):
    if (utils.valid_cpu() or utils.valid_gpu()):
        location = locate.get()
        result, return_value, watt_averages, files = energy(user_func, *args, powerLoss=powerLoss)
        breakdown = energy_mix(location)
        emission, state_emission = emissions(result, breakdown, location)
        utils.log("Assumed Carbon Equivalencies")
        emissions_comparison(result)
        utils.log("Process Energy", result)
        if pdf:
            report.generate(location, watt_averages, breakdown, emission, state_emission)
        if energyOutput:
            return (result, return_value)
        else:
            return return_value

    else:
        utils.log("The energy-usage package only works on Linux kernels "
        "with Intel processors that support the RAPL interface and/or machines with"
        " an Nvidia GPU. Please try again on a different machine.")
