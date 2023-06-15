'''
CSOPESY - CPU Scheduling
Submitted by:
1 - Cai, Edison B.
2 - Muldong, Jericho Luis S.
3 - Susada, Stephanie Joy R.
'''

#FUNCTION FOR FIRST COME FIRST SERVE
def fcfs(y, a, b, c, outputFile):
    '''
    Parameters:
        y (int): Number of processes
        a (list): List of process IDs
        b (list): List of arrival times
        c (list): List of burst times
    '''

    #initialization of variables
    s_t = [0] * y #start time
    e_t = [0] * y # end time
    wt = [0] * y #wait time
    
    s_t[0] = b[0] # start time of first process is always its arrival time
    wt[0] = 0 
    e_t[0] = (s_t[0] + c[0]) #first end time is equal to start time + first burst time
    total_wt = 0 

    with open(outputFile, 'w') as f:
      if b[0] != 0:
        print(f"IDLE start time: 0 end time: {b[0]}")
        f.write(f"IDLE start time: 0 end time: {b[0]}\n")
          
      for i in range(1, y):
          if b[i] > e_t[i-1]:
              # There is a gap of idle time between the end of the previous process 
              # and the start of the current process
              print(f"IDLE start time: {e_t[i-1]} end time: {b[i]}")
              
              f.write(f"IDLE start time: {e_t[i-1]} end time: {b[i]}\n")
              s_t[i] = b[i]
          else:
              s_t[i] = e_t[i-1]
              
          # adding the burst time of the previous process
          #end time
          e_t[i] = s_t[i] + c[i]
          #wait time of the current process
          #   start_time - arrival time
          wt[i] = s_t[i] - b[i]
  
          if wt[i] < 0:
              wt[i] = 0
  
      for i in range(y):
          total_wt = total_wt + wt[i]
          print(str(a[i]) + " start time: " + str(s_t[i]) + " end time: " + str(e_t[i]) + " | Waiting time: " + str(wt[i]))
          f.write(str(a[i]) + " start time: " + str(s_t[i]) + " end time: " + str(e_t[i]) + " | Waiting time: " + str(wt[i]) + "\n")
        
      print("Average waiting time: %.1f" % (total_wt / y))
     
      f.write("Average waiting time: %.1f" % (total_wt / y))

      f.close()
  
def sjf(y, a, b, c, outputFile):
    # Implements Shortest Job First (SJF) CPU scheduling algorithm.
    '''
    Parameters:
        y (int): Number of processes
        a (list): List of process IDs
        b (list): List of arrival times
        c (list): List of burst times
    '''
    #initialization of variable
    waiting_time = [0] * y
    remaining_time = c.copy() #copy of burst time
    start_time = [0] * y
    end_time = [0] * y
    idle_start_time = 0
    idle_end_time = 0

    # Sort the process id by arrival time
    po = sorted(range(len(a)), key=lambda k: b[k])

    current_time = 0
    completed_processes = 0

    with open(outputFile, 'w') as f:
        while completed_processes != y:
            next_process = None
            shortest_burst_time = float('inf')

            for i in range(y):
                if remaining_time[po[i]] > 0 and b[po[i]] <= current_time:
                    if remaining_time[po[i]] < shortest_burst_time:
                        shortest_burst_time = remaining_time[po[i]]
                        next_process = po[i]

            if next_process is None:
                current_time += 1
                if completed_processes == 0 and idle_start_time == 0:
                    idle_start_time = current_time - 1
                elif completed_processes > 0 and idle_start_time > 0:
                    idle_end_time = current_time - 1
                    f.write(f"IDLE start time: {idle_start_time} end time: {idle_end_time}\n")
                    idle_start_time = 0
                    idle_end_time = 0
            else:
                if idle_start_time > 0:
                    idle_end_time = current_time - 1
                    f.write(f"IDLE start time: {idle_start_time - 1} end time: {idle_end_time + 1}\n")
                    idle_start_time = 0
                    idle_end_time = 0
                  
                start_time[next_process] = current_time
                waiting_time[next_process] = current_time - b[next_process]
                current_time += remaining_time[next_process]
                end_time[next_process] = current_time
                remaining_time[next_process] = 0
                completed_processes += 1

        avg_waiting_time = sum(waiting_time) / y

        # Print the results to file
        for i in range(y):
            f.write(f"{i+1} start time: {start_time[i]} end time: {end_time[i]} | Waiting time: {waiting_time[i]}\n")

        f.write(f"Average waiting time: {avg_waiting_time:.1f}\n")
    
    f.close()

#FUNCTION FOR SHORTEST REMAINING TIME FIRST SCHEDULING
def srtf(y, a, b, c, outputFile):
  #Implements Shortest Remaining Time First (SRTF) CPU scheduling algorithm.
  '''
  Parameters:
    y (int): Number of processes
    a (list): List of process IDs
    b (list): List of arrival times
    c (list): List of burst times
  '''
  arr = [[] for i in range(y+1)]  #initializes the list for storing all the start and end times
  pt = [0,0]  #placeholder for the start and end time of a single process run
  clock = 0
  prev_proc = 0
  curr_proc = 0
  idle = True
  switch = False
  idle_switch = False
  waiting = 0
  ave_wt = 0
  
    #iterates until all processes are done
  while any(c):
    #checks if it is currently idling
    if any(c[i] for i in range(y) if b[i] <= clock and c[i] > 0): 
      if idle:
        idle_switch = True
        idle = False
    else:
      if not idle:
        idle = True
        switch = True
  
    if not idle:
      prev_proc = curr_proc + 1
  
        #checks for the shortest remaining burst time when a new process arrives
      for i in range(y):
        if (b[i] <= clock) and (c[i] < c[curr_proc]) and (c[i] > 0):
          curr_proc = i
          switch = True
  
        #checks for the shortest remaining burst time when a process is done
      if (c[curr_proc] == 0):
        if (any(c[i] for i in range(y) if b[i] <= clock and c[i] > 0)):
          curr_proc = c.index(min(c[i] for i in range(y) if b[i] <= clock and c[i] > 0))
          switch = True
      c[curr_proc] -= 1
    
    #marks the start and end times when context switch occurs
    if switch or idle_switch:
      pt[1] = clock
      if idle_switch:
        arr[0].append(pt[:])
        idle_switch = False
      else:
        arr[prev_proc].append(pt[:])
      pt[0] = clock
      switch = False
                  
    clock += 1
  pt[1] = clock
  arr[prev_proc].append(pt[:])
  
  #prints the results
  f = open(outputFile, "w")
  for i in range(y+1):
    if not i:
      f.write("IDLE")
      for j in range(len(arr[i])):
        f.write(" start time: " + str(arr[i][j][0]) + " end time: " + str(arr[i][j][1]) + " |")
    else:
      f.write("\n")
      f.write(str(i))
      for j in range(len(arr[i])):
        f.write(" start time: " + str(arr[i][j][0]) + " end time: " + str(arr[i][j][1]) + " |")
        if j == 0:
          waiting = arr[i][j][0] - b[i-1]
        else:
          waiting = waiting + arr[i][j][0] - arr[i][j-1][1]
      ave_wt += waiting
      f.write(" Waiting time: " + str(waiting))
  ave_wt /= y
  f.write("\n")
  f.write("Average waiting time: " + str(round(ave_wt, 1)))
  f.close()
  

def rr():
  with open(fileName, "r") as file:
      sched_algo, num_processes, time_quantum = map(int, file.readline().split())
      processes = [list(map(int, line.split())) for line in file.readlines()]
  
  burst_times = [column[2] for column in processes]
  all_start_end_time = [[] for i in range(num_processes)] #Variable for storing all start and end times of each process
  
  clock = processes[0][1] #initialize first start time
  ready_queue = []
  waiting_times = []
  
  hasBurst = not all(0 == process[2] for process in processes if len(process) > 2) #check if remaining burst time is not 0 in all processes
  ready_queue.append(processes[0])
  
  while hasBurst:
      curr_process = ready_queue.pop(0) #dequeue process in the head of the queue (first in)
  
      if curr_process[2] != 0: #continue if remaining burst time of the current process is not 0
          if curr_process[2] > time_quantum:
              curr_process[2] -= time_quantum
              
              all_start_end_time[curr_process[0]-1].append([clock, clock + time_quantum]) #store the start time and end time of the current process
  
              clock += time_quantum #update the clock
  
              for i in range(curr_process[0], num_processes):
                  
                  if processes[i][1] <= clock and processes[i][2] > 0 and processes[i] not in ready_queue:
                      ready_queue.append(processes[i]) #place the processes (to the ready queue) that arrived after time quantum
              
              if curr_process[2] != 0 and curr_process not in ready_queue:
                  ready_queue.append(curr_process) #place the current process back in the ready queue since remaining burst time is not 0
  
          elif curr_process[2] <= time_quantum: #if remaining burst time is <= time quantum, set the remaining burst time to 0
              all_start_end_time[curr_process[0]-1].append([clock, clock + curr_process[2]]) #store the start time and end time of the current process
  
              clock += curr_process[2]
  
              if not ready_queue and curr_process[0] < num_processes:
                  ready_queue.append(processes[curr_process[0]])
  
              curr_process[2] = 0
          
          hasBurst = not all(0 == process[2] for process in processes if len(process) > 2) #check if remaining burst time is not 0 in all processes
  
  #print output
  f = open(outputFile, "w")

  for i in range(num_processes):
      toPrint = str(i+1) + " "
      f.write(toPrint)
      print(str(i+1) + " ", end = "")
      for j in range(len(all_start_end_time[i])):
          toPrint = "start time: " + str(all_start_end_time[i][j][0]) + " " + "end time: " + str(all_start_end_time[i][j][1]) + " |"
          f.write(toPrint)
          print("start time: " + str(all_start_end_time[i][j][0]) + " " + "end time: " + str(all_start_end_time[i][j][1]) + " |", end = " ")
          if j == len(all_start_end_time[i]) - 1:
              waiting_time = all_start_end_time[i][j][1] - processes[i][1] - burst_times[i]
              waiting_times.append(waiting_time)
              toPrint = "Waiting time: " + str(str(waiting_time) + "\n")
              f.write(toPrint)
              print("Waiting time: " + str(waiting_time))
  avg_waiting_time = sum(waiting_times)/num_processes
  toPrint = "Average waiting time: " + str(avg_waiting_time)
  f.write(toPrint)
  print("Average waiting time: " + str(avg_waiting_time))

  
#FOR READING INPUTS INSIDE TEXT FILE
fileName = input("Enter the filename: ")
outputFile = input("Enter filename for output: ")
with open(fileName, 'r') as f:
  x, y, z = f.readline().split()
  x = int(x)
  z = int(z)
  y = int(y)
  a = []  # process id
  b = []  # arrival time
  c = []  # burst time

  for i in range(int(y)):
    l, m, n = f.readline().split()
    a.append(int(l))
    b.append(int(m))
    c.append(int(n))

if (x == 0):
  fcfs(y, a, b, c, outputFile)
elif (x == 1):
  sjf(y, a, b, c, outputFile)
elif (x == 2):
  srtf(y, a, b, c, outputFile)
elif (x == 3):
  rr()
