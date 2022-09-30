from email import iterators
from urllib import response
import numpy as np 
from matplotlib import pyplot

def main(filename, params):
    with open(filename, "r") as file:
        lines = file.readlines()

    p95_response_time(lines, params)

def p95_response_time(lines, params):
    p95 = parse_p95_resp_time(lines) 
    time = []

    # Each measurement is from a 10 second interval
    for i in range(len(p95) + 1):
        time.append(i * 10)
    p95.insert(0, 0)


    pyplot.plot(time, p95)
    pyplot.grid()   
    pyplot.xlabel(params[2])
    pyplot.ylabel(params[1])
    pyplot.title(params[0])
    pyplot.show()

def parse_p95_resp_time(lines):
    belongs_to_reponse_time = False
    
    response_time = []

    for line in lines:
        if "http.response_time" in line:
            belongs_to_reponse_time = True
        if "session_length" in line:
            belongs_to_reponse_time = False
        if "p95" in line and belongs_to_reponse_time:
            number = float(line.split(" ")[-1].replace("\n", ""))
            response_time.append(number)
            belongs_to_reponse_time = False
    return response_time

#Matches the length of n arrays to the minimum of them by popping
#elements from longer arrays
def trunc_longer_arrays(arrays):
    lengths = [len(arr) for arr in arrays]
    min_length = np.array(lengths).min()    

    for i in range(len(arrays)):
        for j in range(min_length, len(arrays[i])):
            arrays[i].pop()


#main("stress.txt", ["Stress Test", "Response Time (ms)", "Time (s)"])