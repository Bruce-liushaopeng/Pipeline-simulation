import csv
# constants
insp1_c1_time = 5
insp2_c2_time =10
insp2_c3_time = 15
ws1_time = 10
ws2_time = 12
ws3_time = 9

# states tracking
last_event_time = 0 # this variable is for calculating idle time
clock = 0
block_time = 0
idle_time = 0
w1_idle = 0
w2_idle = 0
w3_idle = 0
bf_c1w1 = 0
bf_c1w2 = 0
bf_c2w2 = 0
bf_c1w3 = 0
bf_c3w3 = 0
p1_produce = 0
p2_produce = 0
p3_produce = 0
lastIsC2 = False # False indicate the next component for Ins2 is C2
w1_aval = True
w2_aval = True
w3_aval = True
evt_queue = [] #(time, event,) ex. (7,ins1c1_end)
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

evt_queue = [(0,ins1c1_start), (0,ins2_start),(699,end_event)] # initial evetn queue

# this function check the buffer condiftion and start workstation accordingly
def workstation_start(): 
    global w1_aval,w2_aval,w3_aval, bf_c1w1,bf_c1w2,bf_c1w3,bf_c2w2,bf_c3w3
    if(w1_aval and bf_c1w1>0):
        evt_queue.append((clock,w1_start))
        w1_aval = False
        bf_c1w1-=1
    if(w2_aval and bf_c2w2>0 and bf_c1w2>0):
        evt_queue.append((clock,w2_start))
        w2_aval = False
        bf_c2w2-=1
        bf_c1w2-=1
    if(w3_aval and bf_c3w3>0 and bf_c1w3>0):
        evt_queue.append((clock,w3_start))
        w3_aval = False
        bf_c3w3-=1
        bf_c1w3-=1

# this function perform the logic to assign c1 to each buffer based on 
# current components in each buffer
def assign_c1():
    global bf_c1w1,bf_c1w2,bf_c1w3
    if(bf_c1w1 == bf_c1w2 == bf_c1w3):
        bf_c1w1+=1
        return 1
    elif(bf_c1w1<=bf_c1w2 and bf_c1w1<=bf_c1w3):
        bf_c1w1+=1
        return 1
    elif(bf_c1w2<=bf_c1w1 and bf_c1w2<=bf_c1w3):
        bf_c1w2+=1
        return 2
    elif(bf_c1w3<=bf_c1w1 and bf_c1w3<=bf_c1w2):
        bf_c1w3+=1
        return 3
    return 0

# return true is buffer for C1 are all full
def is_bfC1_full():
    global bf_c1w1,bf_c1w2,bf_c1w3
    if(bf_c1w1 == bf_c1w2 == bf_c1w3 == 2):
        return True
    return False
    
# this method handles events 
def handle_evt(evt):
    global clock,last_event_time,idle_time, bf_c1w1, block_time, w1_aval, w2_aval, w3_aval, bf_c1w2, bf_c1w3, bf_c2w2, bf_c3w3,p1_produce,p2_produce,p3_produce,ins2_start,lastIsC2,w1_idle,w2_idle,w3_idle
    last_event_time = clock # used to store last clock to calculate idle time
    clock = evt[0]
    print(evt[1] +" at time " +str(clock))
    if(len(evt_queue)>1):
            next_evt_time = evt_queue[0][0]
    else:
        print("no next event")
        exit()
    evt_type = evt[1]

    # inspector 1 start inspect C1
    if(evt_type == ins1c1_start): 
        evt_queue.append((clock + insp1_c1_time,ins1c1_end))

    # inspector 2 start inspect
    elif(evt_type == ins2_start):
        if lastIsC2: # if the last one inspected is C2, this time it will go for C3
            lastIsC2 = False
            evt_queue.append((clock + insp2_c3_time,ins2c3_end))
        else:
            lastIsC2 = True
            evt_queue.append((clock + insp2_c2_time,ins2c2_end))

    # instector 1 finished inspecting C1
    elif(evt_type == ins1c1_end):
        if(is_bfC1_full()):
            evt_queue.append((next_evt_time + 0.1,ins1c1_end))
            block_time += next_evt_time + 0.1- clock
            return
        else:
            assign_c1() #perform logic to assign c1 to the right buffer
            evt_queue.append((clock,ins1c1_start))

    # # instector 2 finished inspecting C2
    elif(evt_type == ins2c2_end):
        if(bf_c2w2 == 2):
            evt_queue.append(( next_evt_time + 0.1, ins2c2_end))
            block_time += next_evt_time + 0.1- clock
        else:
            bf_c2w2 += 1
            #evt_queue.append((clock, w2_start))
            evt_queue.append((clock,ins2_start))

    # instector 2 finished inspecting C3
    elif(evt_type == ins2c3_end):
        if(bf_c3w3 == 2):
            evt_queue.append(( next_evt_time + 0.1, ins2c3_end))
            block_time += next_evt_time + 0.1- clock
        else:
            bf_c3w3 += 1
            evt_queue.append((clock,ins2_start))

    # workstation 1 start 
    elif(evt_type == w1_start):
        evt_queue.append((clock + ws1_time, w1_end))

    # workstation 2 start 
    elif(evt_type == w2_start):
        evt_queue.append((clock + ws2_time, w2_end))
    # workstation 3 start 
    elif(evt_type == w3_start):
        evt_queue.append((clock + ws3_time, w3_end))

    # workstation 1 finished produce 
    elif(evt_type == w1_end):
        p1_produce +=1
        w1_aval = True
    
    # workstation 2 finished produce
    elif(evt_type == w2_end):
        p2_produce+=1
        w2_aval = True

    # workstation 3 finished produce
    elif(evt_type == w3_end):
        p3_produce+=1
        w3_aval = True
    
    # end event and program exit
    elif(evt_type == end_event):
        print(end_event)
        print("------------------------------------------------------------")
        print("state_tracking.csv generated, please check for more detail")
        print("------------------------------------------------------------")
        exit()
    workstation_start() #check if components are ready, if yes, start the workstation accordingly
    if w1_aval:
        idle_time += (clock - last_event_time)
        w1_idle += (clock - last_event_time)
    if w2_aval:
        idle_time += (clock - last_event_time)
        w2_idle += (clock - last_event_time)
    if w3_aval:
        idle_time += (clock - last_event_time)
        w3_idle += (clock - last_event_time)

# start simulation
def start():
    import csv
    # generating csv file to keep track of states
    with open('state_tracking.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Clock", "C1_W1","C1W2","C1W3","C2W2","C3W3", "Part1","Part2","Part3","Total Block Time","w1_idle","w2_idle","w3_idle","Total Idle Time(workstation)","w1_aval","w2_aval","w3_aval","Event Queue"])
        while(len(evt_queue) > 0 ):
            evt_queue.sort()
            eventLeft = ""
            for event in evt_queue:
                eventLeft+='(' +str(event[0]) + ', '+event[1]+') '
            evt = evt_queue.pop(0)
            handle_evt(evt)
            writer.writerow([clock, bf_c1w1,bf_c1w2,bf_c1w3,bf_c2w2,bf_c3w3,p1_produce,p2_produce,p3_produce,block_time,w1_idle,w2_idle,w3_idle,idle_time,w1_aval,w2_aval,w3_aval,str(eventLeft)])
    

start()