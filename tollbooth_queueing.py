import numpy as np
import matplotlib.pyplot as plt

# Adapated from queuing code provided by Dr. McSweeney in the Spring 2025-26 seciton of MA445
def simulate(rate_in, rates_out, time_to_sim, driver_decision_func):
    if(rate_in >= sum(rates_out)):
        print("Arrival rate is higher than service rate, so entry congestion will grow indefinitely.")
        return [], []
    
    num_booths = len(rates_out)
    driver_seq = [[0 for n in range(num_booths)]]   #sequence of numbers of customers
    drivers = [0 for n in range(num_booths)]  #current number of customers
    cur_time = 0
    time_seq = [0]

    

    while(cur_time < time_to_sim):   
        u = np.random.random()
        total_service_rate = 0
        total_drivers = 0
        for n in range(num_booths):
            if(drivers[n] > 0): total_service_rate += rates_out[n]
            total_drivers += drivers[n]

        cur_prob = 0
        # Determine if random event is arrival or departure
        for i in range(-1, num_booths):
            if(i == -1): cur_prob += rate_in / (rate_in + total_service_rate)
            elif(drivers[i] > 0): cur_prob += rates_out[i] / (rate_in + total_service_rate)

            if(cur_prob >= u):
                if(i == -1):
                    lane_enterred = driver_decision_func(drivers)
                    drivers[lane_enterred] += 1
                    break
                else:
                    drivers[i] -= 1
                    break
        
        driver_seq.append(drivers.copy())  # Track history of # in queue
        current_wait = np.random.exponential(rate_in + total_service_rate)     # Time until event occured
        cur_time += current_wait
        time_seq.append(cur_time)  #keeping track of all event times
    
    return driver_seq, time_seq

def rand_choice(lanes):
    return np.random.randint(0, len(lanes) )

def plot(drivers, times):
    fig, ax1 = plt.subplots(figsize=(13, 7))

    drivers = np.array(drivers).T

    colors = ["red", "blue", "green"] # extend
    for i in range(len(drivers)):
        ax1.plot(times, drivers[i], label=f'# in queue {i}')

    ax1.set_xlabel("Time")
    ax1.set_ylabel("Queue Lengths")
    ax1.legend(loc='best')

    plt.title(f"Queue Lengths of Time")
    plt.tight_layout()
    
    plt.show()


drivers, times = simulate(20, [12, 12, 6, 6], 25000, rand_choice)

plot(drivers, times)


