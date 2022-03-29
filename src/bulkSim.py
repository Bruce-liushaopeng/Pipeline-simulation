from sim import Sim
from sim_summary import simSummary
import csv

numSim = input("How many simulation to run? ")
numSim = int(numSim)
summaryList = []
count = 1
with open('bulk_summary.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "seed","simulation time","warmup period" ,"Part1","Part2","Part3","inspector1 block time","inspector2 block time","inspector3 block time","Total Block Time","workstation1 idle time","workstation2 idle time","workstation3 idle time","Total Idle Time(workstation)"])
            while(count<numSim+1):
                print("simulation " + str(count) + "...")
                mySim = Sim(count)
                mySummary = mySim.start()
                summaryList.append(mySummary)
                writer.writerow([count,count,5000,1000,mySummary.p1,mySummary.p2,mySummary.p3,mySummary.ins2_block_time,mySummary.ins2_block_time,mySummary.ins3_block_time,mySummary.total_block_time,mySummary.w1_idle,mySummary.w2_idle,mySummary.w3_idle,mySummary.w1_idle+mySummary.w2_idle+mySummary.w3_idle])
                count +=1

sum_ins1_block=0
sum_ins2_block=0
sum_ins3_block=0
sum_total_block=0
sum_w1_idle=0
sum_w2_idle=0
sum_w3_idle=0
sum_total_idle_workstation=0
p1_sum=0
p2_sum=0
p3_sum=0

for summary in summaryList:
    sum_ins1_block += summary.ins1_block_time
    sum_ins2_block += summary.ins2_block_time
    sum_ins3_block += summary.ins3_block_time
    p1_sum += summary.p1
    p2_sum += summary.p2
    p3_sum += summary.p3
    sum_w1_idle += summary.w1_idle
    sum_w2_idle += summary.w2_idle
    sum_w3_idle += summary.w3_idle
    sum_total_idle_workstation += (summary.w1_idle + summary.w2_idle+summary.w3_idle)

avg_p1 = p1_sum / numSim
avg_p2 = p2_sum / numSim
avg_p3 = p3_sum / numSim
avg_ins1_block = sum_ins1_block / numSim
avg_ins2_block = sum_ins2_block / numSim
avg_ins3_block = sum_ins3_block / numSim
avg_w1_idle = sum_w1_idle / numSim
avg_w2_idle = sum_w2_idle / numSim
avg_w3_idle = sum_w3_idle / numSim
avg_workstation_idle = sum_total_idle_workstation / numSim

print("p1 produced in average : " + str(avg_p1))
print("p1 produced in average : " + str(avg_p2))
print("p1 produced in average : " + str(avg_p3))
print("mean inspector 1 block time : " + str(avg_ins1_block))
print("mean inspector 2 block time : " + str(avg_ins2_block))
print("mean inspector 3 block time : " + str(avg_ins3_block))
print("mean workstation 1 idle time : " + str(avg_w1_idle))
print("mean workstation 2 idle time : " + str(avg_w2_idle))
print("mean workstation 3 idle time : " + str(avg_w3_idle))

