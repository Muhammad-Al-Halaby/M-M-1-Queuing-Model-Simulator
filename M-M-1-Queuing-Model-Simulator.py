# M/M/1 Queuing Model Simulator
# Author: Muhammad Al-Halaby
# Created: 27-Dec-2019

import numpy
import math
import matplotlib.pyplot as graph

# First Specify:
# 1- the customers’ arrival rate (λ)
# 2- the customers’ service rate (μ)
# 3- the number of customers (samples) involved in the simulation.
arrival_rate = 30
service_rate = 40
number_of_customers = 1000

# Data to be generated
inter_arrival_time = []
arrival_time = []
service_time = []

# Data to be calculated
finishing_time = []
total_time = []
waiting_time = []
queue_length_per_time = []
queue_length_per_customer = []
max_finishing_time = 0

# ------------------------------------------------------------- #

# Generate inter-arrival times
inter_arrival_time = 1 / (numpy.random.poisson(arrival_rate, number_of_customers) + 1)

# Calculate arrival time through the cumulative sum of inter-arrival times
arrival_time = numpy.cumsum(inter_arrival_time)

# Generate service time
service_time = numpy.random.exponential(1 / service_rate, number_of_customers)

# Calculate finishing time
finishing_time = arrival_time + service_time
for i in range(1, number_of_customers):
    finishing_time[i] = max(finishing_time[i], finishing_time[i - 1] + service_time[i])

# Calculate total time
total_time = finishing_time - arrival_time

# Calculate waiting time
waiting_time = total_time - service_time

# Calculate the length of the queue at every unit of time
max_finishing_time = math.ceil(finishing_time[number_of_customers - 1] + 2)
for i in range(max_finishing_time):
    queue_length_per_time.append(0)

for i in range(number_of_customers):
    a = math.ceil(arrival_time[i])
    b = math.ceil(arrival_time[i] + waiting_time[i])
    if a == b:  b += 1;
    queue_length_per_time[a] += 1
    queue_length_per_time[b] -= 1

for i in range(1, math.ceil(finishing_time[number_of_customers - 1] + 1)):
    queue_length_per_time[i] += queue_length_per_time[i - 1]

# Calculate the length of the queue at customer arrival times
for i in range(number_of_customers):
    queue_length_per_customer.append(queue_length_per_time[math.ceil(arrival_time[i])])

# Calculate mean of arrival rates (λ), mean of service rates (μ) and utilization rate (ρ)
mean_arrival_rate = round(1 / (sum(inter_arrival_time) / number_of_customers))
mean_service_rate = round(1 / (sum(service_time) / number_of_customers))
utilization_rate = round(mean_arrival_rate / mean_service_rate * 100, 2)

# --------------------------------Plotting Data----------------------------------- #
message = "                  No. of customers = " + str(number_of_customers) \
          + "   λ = " + str(mean_arrival_rate) \
          + "   μ = " + str(mean_service_rate) \
          + "   ρ = " + str(utilization_rate) + "%"
graph.subplots_adjust(top=0.8)
graph.gcf().text(0.02, 0.9, message, fontsize=14)

graph.subplot(3, 3, 1)
graph.plot(list(range(number_of_customers)), total_time)
graph.xlabel('Customer Number')
graph.ylabel('Total Time [m]')
graph.title('Total Time / Customer')

graph.subplot(3, 3, 3)
graph.plot(list(range(number_of_customers)), waiting_time)
graph.xlabel('Customer Number')
graph.ylabel('Waiting Time [m]')
graph.title('Waiting Time / Customer')

graph.subplot(3, 3, 7)
graph.plot(list(range(max_finishing_time)), queue_length_per_time)
graph.xlabel('Time [m]')
graph.ylabel('Queue Length')
graph.title('Queue length / Time')

graph.subplot(3, 3, 9)
graph.plot(list(range(number_of_customers)), queue_length_per_customer)
graph.xlabel('Customer Number')
graph.ylabel('Queue Length')
graph.title('Queue length / Customer Arrival')

graph.gcf().canvas.set_window_title("M/M/1 Queuing Model Simulator - Muhammad Al-Halaby")
graph.show()
