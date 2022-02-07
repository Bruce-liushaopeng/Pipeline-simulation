# constants
insp1_c1_time = 5
insp2_c2_time =15
insp2_c3_time = 20
ws1_time = 5
ws2_time = 11
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
lastIsC2 = True # true indicate the next component for Ins2 is C3
w1_aval = True
w2_aval = True
w3_aval = True
evt_queue = [] #(time, event,) ex. (7,ins1c1_end)
# events identifier
ins1c1_start = "inspctor 1 start to inspect component 1"
ins2c2_start = "inspctor 2 start to inspect component 2"
ins2c3_start = "inspctor 2 start to inspect component 3"
ins1c1_end = "inspctor 1 finished to inspect component 1"
ins2c2_end = "inspctor 2 finished to inspect component 2"
ins2c3_end = "inspctor 2 finished to inspect component 3"

w1_start = "Workstation 1 start to produce Part 1"
w2_start = "Workstation 2 start to produce Part 2"
w3_start = "Workstation 3 start to produce Part 3"
w1_end = "Workstation 1 finished to produce Part 1"
w2_end = "Workstation 2 finished to produce Part 2"
w3_end = "Workstation 3 finished to produce Part 3"
end_event = "system end"

evt_queue = [(0,ins1c1_start), (0,ins2c2_start),(10,ins1c1_start),(60,end_event)] # initial evetn queue

def assign_c1():
    global bf_c1w1,bf_c1w2,bf_c1w3
    if(bf_c1w1 == bf_c1w2 == bf_c1w3):
        bf_c1w1+=1
        return 1
    elif(bf_c1w1<bf_c1w2 and bf_c1w1<bf_c1w3):
        bf_c1w1+=1
        return 1
    elif(bf_c1w2<bf_c1w1 and bf_c1w2<bf_c1w3):
        bf_c1w2+=1
        return 2
    elif(bf_c1w3<bf_c1w1 and bf_c1w3<bf_c1w2):
        bf_c1w3+=1
        return 3
    return 0

def is_bfC1_full():
    global bf_c1w1,bf_c1w2,bf_c1w3
    if(bf_c1w1 == bf_c1w2 == bf_c1w3 == 2):
        return True
    return False
    

def handle_evt(evt):
    global clock,bf_c1w1, block_time, bf_c1w2,bf_c2w2
    print(evt[1] +" at time " +str(clock))
    print("length of event queue is " + str(len(evt_queue)))
    if(len(evt_queue)>1):
            next_evt_time = evt_queue[0][0]
    clock = evt[0]
    evt_type = evt[1]
    if(evt_type == ins1c1_start):
        evt_queue.append((clock + insp1_c1_time,ins1c1_end))
        print("create end evetn for ins1")

    elif(evt_type == ins2c2_start):
        evt_queue.append((clock + insp2_c2_time,ins2c2_end))
        print("create end event for ins2")
    
    if(evt_type == ins1c1_end):
        if(is_bfC1_full()):
            evt_queue.append((clock + next_evt_time + 0.01,ins1c1_end))
            block_time += next_evt_time - clock
            return
        else:
            c1_assigned = assign_c1()
            if(c1_assigned == 1):
                evt_queue.append((clock,w1_start))
            elif(c1_assigned == 2):
                evt_queue.append((clock,w2_start))
            elif(c1_assigned == 3):
                evt_queue.append((clock,w3_start))
            evt_queue.append((clock,ins1c1_start))

    elif(evt_type == w1_start):
        if(w1_aval and bf_c1w1>0):
            bf_c1w1 -=1
            evt_queue.append((clock + ws1_time, w1_end))
        else:
            evt_queue.append((clock + next_evt_time, w1_start))

    elif(evt_type == w2_start):
        if(w2_aval and bf_c2w2>0 and bf_c1w2>0):
            bf_c1w2 -=1
            bf_c2w2 -=1
            evt_queue.append((clock + ws2_time, w2_end))
        else:
            evt_queue.append((clock + next_evt_time, w2_start))
    elif(evt_type == end_event):
        print(end_event)
        exit()


    

        

def start():
    while(len(evt_queue) > 0 ):
        evt_queue.sort(reverse=True)
        evt = evt_queue.pop()
        handle_evt(evt)


start()