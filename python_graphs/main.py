import base64
import requests

def req(link):
  master = "https://raw.githubusercontent.com/LordOfThePing/2c22-tp-1-aquitectura/graficos-python/python_graphs/" + link
  return requests.get(master).text

ping_breakpoint = req("ping/breakpoint.txt")
ping_stress = req("ping/stress.txt")
ping_endurance = req("ping/endurance.txt")

from email import iterators
from urllib import response
import numpy as np 
from matplotlib import pyplot

pyplot.rcParams['figure.figsize'] = [15, 5]




#def main(filename, params, i):
    #with open(filename, "r") as file:
    #    lines = file.readlines()

def main(strfile, title, graphs):


    i = 0
    #pyplot.figure(i)
    pyplot.title(title)
    for graph in graphs:
      i = i+1
      pyplot.subplot(1,2, i)
      lines = iter(strfile.splitlines())

      graph[0](lines, graph)

    pyplot.show()


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


def plot_number_of_requests(lines, params):
    reqs = parse_num_of_reqs(lines) 
    time = []
    # Each measurement is from a 10 second interval
    for i in range(len(reqs) + 1):
        time.append(i * 10)
    reqs.insert(0, 0)

    pyplot.plot(time, reqs)
    pyplot.grid()   
    pyplot.xlabel(params[2])
    pyplot.ylabel(params[1])



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
        if "Summary report" in line:
            break
        
    return response_time

def parse_num_of_reqs(lines):
    requests = []

    for line in lines:
        if "http.requests" in line:
            number = float(line.split(" ")[-1].replace("\n", ""))
            requests.append(number)
        if "Summary report" in line:
            break
    return requests
    
#Matches the length of n arrays to the minimum of them by popping
#elements from longer arrays
def trunc_longer_arrays(arrays):
    lengths = [len(arr) for arr in arrays]
    min_length = np.array(lengths).min()    

    for i in range(len(arrays)):
        for j in range(min_length, len(arrays[i])):
            arrays[i].pop()


#main("stress.txt", ["Stress Test", "Response Time (ms)", "Time (s)"])
