import csv
import math
import random
from timeGenerator import timeGenerator
from sim_summary import simSummary as simSummmary
# events identifier
ins1c1_start = "ins1c1_start"
ins2_start = "ins2_start"
ins1c1_end = "ins1c1_end"
ins2c2_end = "ins2c2_end"
ins2c3_end = "ins2c3_end"

w1_start = "w1_start"
w2_start = "w2_start"
w3_start = "w3_start"
w1_end = "w1_end"
w2_end = "w2_end"
w3_end = "w3_end"
end_event = "system end"
class Sim:
    def __init__(self,seed) -> None:
        # constants
        self.myTimeGenerator = timeGenerator(seed)
        # states tracking
        self.last_event_time = 0 # this variable is for calculating idle time
        self.clock = 0
        self.notResetYet = True
        self.ins1_block_time = 0
        self.ins2_block_time = 0
        self.ins3_block_time = 0
        self.block_time = 0
        self.idle_time = 0
        self.w1_idle = 0
        self.w2_idle = 0
        self.w3_idle = 0
        self.bf_c1w1 = 0
        self.bf_c1w2 = 0
        self.bf_c2w2 = 0
        self.bf_c1w3 = 0
        self.bf_c3w3 = 0
        self.p1_produce = 0
        self.p2_produce = 0
        self.p3_produce = 0
        self.w1_aval = True
        self.w2_aval = True
        self.w3_aval = True
        self.programStop = False
        self.evt_queue = [(0,ins1c1_start), (0,ins2_start),(5000,end_event)] #(time, event,) ex. (7,ins1c1_end)
   
    def reset(self):
        self.ins1_block_time = 0
        self.ins2_block_time = 0
        self.ins3_block_time = 0
        self.block_time = 0
        self.idle_time = 0
        self.w1_idle = 0
        self.w2_idle = 0
        self.w3_idle = 0
        self.p1_produce = 0
        self.p2_produce = 0
        self.p3_produce = 0


    # this function check the buffer condiftion and start workstation accordingly
    def workstation_start(self): 
        if(self.w1_aval and self.bf_c1w1>0):
            self.evt_queue.append((self.clock,w1_start))
            self.w1_aval = False
            self.bf_c1w1-=1
        if(self.w2_aval and self.bf_c2w2>0 and self.bf_c1w2>0):
            self.evt_queue.append((self.clock,w2_start))
            self.w2_aval = False
            self.bf_c2w2-=1
            self.bf_c1w2-=1
        if(self.w3_aval and self.bf_c3w3>0 and self.bf_c1w3>0):
            self.evt_queue.append((self.clock,w3_start))
            self.w3_aval = False
            self.bf_c3w3-=1
            self.bf_c1w3-=1

    # this function perform the logic to assign c1 to each buffer based on 
    # current components in each buffer
    def assign_c1(self):
        if(self.bf_c1w1 == self.bf_c1w2 == self.bf_c1w3):
            self.bf_c1w1+=1
            return 1
        elif(self.bf_c1w1<=self.bf_c1w2 and self.bf_c1w1<=self.bf_c1w3):
            self.bf_c1w1+=1
            return 1
        elif(self.bf_c1w2<=self.bf_c1w1 and self.bf_c1w2<=self.bf_c1w3):
            self.bf_c1w2+=1
            return 2
        elif(self.bf_c1w3<=self.bf_c1w1 and self.bf_c1w3<=self.bf_c1w2):
            self.bf_c1w3+=1
            return 3
        return 0

    # return true is buffer for C1 are all full
    def is_bfC1_full(self):
        if(self.bf_c1w1 == self.bf_c1w2 == self.bf_c1w3 == 2):
            return True
        return False
        
    # this method handles events 
    def handle_evt(self,evt):
        if(abs(self.clock-1000)<10 and self.notResetYet):
            self.notResetYet = False
            self.reset()
        self.last_event_time = self.clock # used to store last self.clock to calculate idle time
        self.clock = evt[0]
        #print(evt[1] +" at time " +str(self.clock))
        if(len(self.evt_queue)>1):
                next_evt_time = self.evt_queue[0][0]
        else:
            #print("no next event")
            self.programStop = True
        evt_type = evt[1]

        # inspector 1 start inspect C1
        if(evt_type == ins1c1_start): 
            self.evt_queue.append((self.clock + self.myTimeGenerator.getIns1Time(),ins1c1_end))

        # inspector 2 start inspect
        elif(evt_type == ins2_start):
            two_or_three = random.random()
            if two_or_three > 0.5:
                self.evt_queue.append((self.clock + self.myTimeGenerator.getIns3Time(),ins2c3_end))
            else:
                self.evt_queue.append((self.clock + self.myTimeGenerator.getIns2Time(),ins2c2_end))

        # instector 1 finished inspecting C1
        elif(evt_type == ins1c1_end):
            if(self.is_bfC1_full()):
                self.evt_queue.append((next_evt_time + 0.1,ins1c1_end))
                self.block_time += next_evt_time + 0.1- self.clock
                self.ins1_block_time += next_evt_time + 0.1- self.clock
                return
            else:
                self.assign_c1() #perform logic to assign c1 to the right buffer
                self.evt_queue.append((self.clock,ins1c1_start))

        # # instector 2 finished inspecting C2
        elif(evt_type == ins2c2_end):
            if(self.bf_c2w2 == 2):
                self.evt_queue.append(( next_evt_time + 0.1, ins2c2_end))
                self.block_time += next_evt_time + 0.1- self.clock
                self.ins2_block_time += next_evt_time + 0.1- self.clock
            else:
                self.bf_c2w2 += 1
                self.evt_queue.append((self.clock,ins2_start))

        # instector 2 finished inspecting C3
        elif(evt_type == ins2c3_end):
            if(self.bf_c3w3 == 2):
                self.evt_queue.append(( next_evt_time + 0.1, ins2c3_end))
                self.block_time += next_evt_time + 0.1- self.clock
                self.ins3_block_time += next_evt_time + 0.1- self.clock
            else:
                self.bf_c3w3 += 1
                self.evt_queue.append((self.clock,ins2_start))

        # workstation 1 start 
        elif(evt_type == w1_start):
            self.evt_queue.append((self.clock + self.myTimeGenerator.getWs1Time(), w1_end))

        # workstation 2 start 
        elif(evt_type == w2_start):
            self.evt_queue.append((self.clock + self.myTimeGenerator.getWs2Time(), w2_end))
        # workstation 3 start 
        elif(evt_type == w3_start):
            self.evt_queue.append((self.clock + self.myTimeGenerator.getWs3Time(), w3_end))

        # workstation 1 finished produce 
        elif(evt_type == w1_end):
            self.p1_produce +=1
            self.w1_aval = True
        
        # workstation 2 finished produce
        elif(evt_type == w2_end):
            self.p2_produce+=1
            self.w2_aval = True

        # workstation 3 finished produce
        elif(evt_type == w3_end):
            self.p3_produce+=1
            self.w3_aval = True
        
        # end event and program exit
        elif(evt_type == end_event):
            #print(end_event)
            #print("------------------------------------------------------------")
            #print("state_tracking.csv generated, please check for more detail")
            #print("------------------------------------------------------------")
            self.programStop = True
        self.workstation_start() #check if components are ready, if yes, start the workstation accordingly
        if self.w1_aval:
            self.idle_time += (self.clock - self.last_event_time)
            self.w1_idle += (self.clock - self.last_event_time)
        if self.w2_aval:
            self.idle_time += (self.clock - self.last_event_time)
            self.w2_idle += (self.clock - self.last_event_time)
        if self.w3_aval:
            self.idle_time += (self.clock - self.last_event_time)
            self.w3_idle += (self.clock - self.last_event_time)

    # start simulation
    def start(self):
        import csv
        # generating csv file to keep track of states
        with open('state_tracking.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["self.Clock", "C1_W1","C1W2","C1W3","C2W2","C3W3", "Part1","Part2","Part3","inspector1 block time","inspector2 block time","inspector3 block time","Total Block Time","self.w1_idle","self.w2_idle","self.w3_idle","Total Idle Time(workstation)","self.w1_aval","self.w2_aval","self.w3_aval","Event Queue"])
            while(len(self.evt_queue) > 0 and not self.programStop):
                self.evt_queue.sort()
                eventLeft = ""
                for event in self.evt_queue:
                    eventLeft+='(' +str(event[0]) + ', '+event[1]+') '
                evt = self.evt_queue.pop(0)
                self.handle_evt(evt)
                writer.writerow([self.clock, self.bf_c1w1,self.bf_c1w2,self.bf_c1w3,self.bf_c2w2,self.bf_c3w3,self.p1_produce,self.p2_produce,self.p3_produce,self.ins1_block_time,self.ins2_block_time,self.ins3_block_time,self.block_time,self.w1_idle,self.w2_idle,self.w3_idle,self.idle_time,self.w1_aval,self.w2_aval,self.w3_aval,str(eventLeft)])
        
        summary = simSummmary(self.ins1_block_time,self.ins2_block_time,self.ins3_block_time,self.block_time,self.w1_idle,self.w2_idle,self.w3_idle,self.p1_produce,self.p2_produce,self.p3_produce)
        #print("sim complete")
        return summary
