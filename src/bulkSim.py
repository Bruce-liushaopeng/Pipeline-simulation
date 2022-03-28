from sim import Sim
from sim_summary import simSummary
import csv

numSim = input("How many simulation to run? ")
numSim = int(numSim)

count = 1
with open('bulk_summary.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "seed","simulation time" ,"Part1","Part2","Part3","inspector1 block time","inspector2 block time","inspector3 block time","Total Block Time","workstation1 idle time","workstation2 idle time","workstation3 idle time","Total Idle Time(workstation)"])
            while(count<numSim+1):
                print("count " + str(count))
                mySim = Sim(count)
                mySummary = mySim.start()
                writer.writerow([count,count,5000,mySummary.p1,mySummary.p2,mySummary.p3,mySummary.total_block_time,mySummary.w1_idle,mySummary.w2_idle,mySummary.w3_idle,mySummary.w1_idle+mySummary.w2_idle+mySummary.w3_idle])
                count +=1