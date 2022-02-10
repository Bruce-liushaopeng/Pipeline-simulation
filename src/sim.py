import csv
# constants
insp1_c1_time = 5
insp2_c2_time =10
insp2_c3_time = 15
ws1_time = 10
ws2_time = 12
ws3_time = 9

# states tracking
clock = 0
block_time = 0
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
        w2_aval = False
        bf_c3w3-=1
        bf_c1w3-=1

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

def is_bfC1_full():
    global bf_c1w1,bf_c1w2,bf_c1w3
    if(bf_c1w1 == bf_c1w2 == bf_c1w3 == 2):
        return True
    return False
    

def handle_evt(evt):
    '''
    Concern about adding event w2_start and w3_start.
    I think it is better to create event at the end of this function. 
    having another if statement to check if buffer c1w2 and c2w2 has enough component to assemble product
    '''
    global clock, bf_c1w1, block_time, w1_aval, w2_aval, w3_aval, bf_c1w2, bf_c1w3, bf_c2w2, bf_c3w3,p1_produce,p2_produce,p3_produce,ins2_start,lastIsC2
    clock = evt[0]
    print("queue length is " + str(len(evt_queue)))
    print(evt[1] +" at time " +str(clock))
    print("length of event queue is " + str(len(evt_queue)))
    if(len(evt_queue)>1):
            next_evt_time = evt_queue[0][0]
    else:
        print("no next event")
        exit()
    evt_type = evt[1]
    if(evt_type == ins1c1_start):
        evt_queue.append((clock + insp1_c1_time,ins1c1_end))

    elif(evt_type == ins2_start):
        if lastIsC2:
            lastIsC2 = False
            evt_queue.append((clock + insp2_c3_time,ins2c3_end))
        else:
            lastIsC2 = True
            evt_queue.append((clock + insp2_c2_time,ins2c2_end))

    elif(evt_type == ins1c1_end):
        if(is_bfC1_full()):
            evt_queue.append((next_evt_time + 0.1,ins1c1_end))
            block_time += next_evt_time + 0.1- clock
            return
        else:
            c1_assigned = assign_c1()
           #if(c1_assigned == 1):
           #     evt_queue.append((clock,w1_start))
           # elif(c1_assigned == 2):
           #     evt_queue.append((clock,w2_start))
           # elif(c1_assigned == 3):
           #     evt_queue.append((clock,w3_start))
            evt_queue.append((clock,ins1c1_start))

    elif(evt_type == ins2c2_end):
        if(bf_c2w2 == 2):
            evt_queue.append(( next_evt_time + 0.1, ins2c2_end))
            block_time += next_evt_time + 0.1- clock
        else:
            bf_c2w2 += 1
            #evt_queue.append((clock, w2_start))
            evt_queue.append((clock,ins2_start))

    elif(evt_type == ins2c3_end):
        if(bf_c3w3 == 2):
            evt_queue.append(( next_evt_time + 0.1, ins2c3_end))
            block_time += next_evt_time + 0.1- clock
        else:
            bf_c3w3 += 1
            evt_queue.append((clock,ins2_start))

    elif(evt_type == w1_start):
        evt_queue.append((clock + ws1_time, w1_end))

    elif(evt_type == w2_start):
        evt_queue.append((clock + ws2_time, w2_end))
    
    elif(evt_type == w3_start):
        evt_queue.append((clock + ws3_time, w3_end))

    elif(evt_type == w1_end):
        p1_produce +=1
        w1_aval = True
    
    elif(evt_type == w2_end):
        p2_produce+=1
        w2_aval = True

    elif(evt_type == w3_end):
        p3_produce+=1
        w3_aval = True

    elif(evt_type == end_event):
        print(end_event)
        exit()
    workstation_start() #check if components are ready, if yes, start the workstation accordingly
    
    


def start():
    import csv
    with open('state_tracking.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Clock", "C1_W1","C1W2","C1W3","C2W2","C3W3", "Part1","Part2","Part3","Total Block Time" "Event Queue"])
        while(len(evt_queue) > 0 ):
            evt_queue.sort()
            eventLeft = ""
            for event in evt_queue:
                eventLeft+='(' +str(event[0]) + ', '+event[1]+') '
            evt = evt_queue.pop(0)
            handle_evt(evt)
            writer.writerow([clock, bf_c1w1,bf_c1w2,bf_c1w3,bf_c2w2,bf_c3w3,p1_produce,p2_produce,p3_produce,block_time,str(eventLeft)])


start()