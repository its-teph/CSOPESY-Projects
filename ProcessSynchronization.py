import threading
import time
import random

# Constants corresponding to the colors of the threads
BLUE = "Blue"
GREEN = "Green"

def fit_clothes():
    time.sleep(1)


print("OS Process Synchronization\n")

slots = int(input("Enter the number of slots inside the fitting room: "))
if slots <= 0:
   print("The number of slots should be positive.")

num_blue = int(input("Enter the number of blue threads: "))
if num_blue < 0:
    print("The number of blue threads should be nonnegative.")

num_green = int(input("Enter the number of green threads: "))
if num_green < 0:
    print("The number of green threads should be nonnegative.")

if num_blue == 0 and num_green == 0:
   print("No threads to synchronize!")

class Lightswitch:
    def __init__(self, color):
        self.counter = 0                        
        self.color = color                      
        self.mutex = threading.Semaphore(1)

    def lock(self, blue_green_mutex):
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            blue_green_mutex.acquire()
        self.mutex.release()

    def unlock(self, blue_green_mutex):
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            blue_green_mutex.release()
        self.mutex.release()


blue_green_mutex = threading.Semaphore(1)             
turnstile = threading.Semaphore(1) 

blue_in_room = Lightswitch(BLUE)
green_in_room = Lightswitch(GREEN)

num_allowed_blue = threading.Semaphore(slots)
num_allowed_green = threading.Semaphore(slots)

# ID of the current thread
# The nth thread to enter the fitting room is assigned the ID n.
thread_id = 0

# Number of threads in the fitting room
room_ctr = 0

# Mutex lock that ensures the atomicity of selected operations in a thread's activity
# Refer to the documentation of blue_thread_func() and green_thread_func() for the particulars
# of these operations.
room_mutex = threading.Lock()


# ---------------------------
#   THREAD TARGET FUNCTIONS
# ---------------------------

# Method corresponding to the activity of a blue thread
def blue_thread_func():
    # Provide access to the shared variables.
    global thread_id, room_ctr

    # Use the turnstile and lightswitch synchronization design patterns to prevent starvation
    # and allow multiple blue threads to concurrently enter the fitting room while blocking
    # green threads:
    #   - Once a blue thread acquires the turnstile while blue threads are in the fitting room,
    #     the lightswitch blue_in_room will "waitlist" its entry. It is the job of the num_allowed_blue
    #     multiplexer to block its entry if the fittign room is full.
    #   - Once a green thread acquires the turnstile while blue threads are in the fitting room,
    #     the lightswitch blue_in_room will block this thread. Therefore, the turnstile will not
    #     be released as long as this thread is blocked, effectively blocking all incoming threads
    #     and preventing starvation.
    turnstile.acquire()
    blue_in_room.lock(blue_green_mutex)
    turnstile.release()

    # Following the multiplexer pattern, decrement the number of blue threads that can enter the
    # fitting room. If the value of this counting semaphore drops to 0, then acquiring it will
    # block that acquiring thread.

    # As opposed to this releasing this num_allowed_blue semaphore, note that acquiring it should
    # not be inside any mutex lock. Waiting on a semaphore inside a mutex lock is a well-known
    # deadlock pattern, as a thread blocking on this semaphore will prevent the mutex lock from
    # being released.
    num_allowed_blue.acquire()

    # Local variable for storing the ID of the current thread
    current_thread_id = None

    # To prevent other blue threads in the fitting room from interleaving and possibly resulting
    # in the IDs, counters, and display messages to be out of sync, ensure the atomicity of the
    # following sequence of operations:
    #   - Incrementing the thread ID
    #   - Incrementing the number of threads in the fitting room
    #   - Displaying the message associated with the entry of the first thread into an empty
    #     fitting room
    #   - Setting the thread ID of the current active thread
    #   - Displaying the message associated with the entry of a thread
    with room_mutex:
        thread_id += 1
        room_ctr += 1

        # Display the message associated with the entry of the first thread into an empty fitting room.
        if room_ctr == 1:
            safe_print(f"----- {BLUE} Only -----\n")

        current_thread_id = thread_id

        # Display the message associated with the entry of a thread.
        safe_print(f"Thread ID: {current_thread_id}\nColor: {BLUE}\n")

    # Simulate the stay of the blue thread inside the fitting room for an arbitrary duration.
    fit_clothes()

    # To prevent other blue threads in the fitting room from interleaving and possibly resulting
    # in the IDs, counters, and display messages to be out of sync, ensure the atomicity of the
    # following sequence of operations:
    #   - Incrementing the counting semaphore denoting the number of blue threads that can enter
    #     the fitting room
    #   - Decrementing the number of threads in the fitting room
    #   - Displaying the message associated with the exit of a thread
    #   - Displaying the message associated with an empty fitting room
    
    # The room_mutex lock (instead of creating a new lock) is used in order to ensure that the
    # number of threads in the fitting room is first incremented (room_ctr += 1) before it is
    # decremented (room_ctr -= 1), preventing it from assuming an illogical negative value.
    with room_mutex:
        num_allowed_blue.release()
        room_ctr -= 1

        # Display the message associated with the exit of a thread.
        # This allows the user to track the threads in the fitting room.
        safe_print(f"Thread {current_thread_id} exits the fitting room.\n")

        # Display the message associated with an empty fitting room.
        if room_ctr == 0:
            safe_print(">> Empty Fitting Room\n")

    # Invoke the unlock() method of the blue threads' lightswitch.
    blue_in_room.unlock(blue_green_mutex)


# Method corresponding to the activity of a green thread
def green_thread_func():
    # Provide access to the shared variables.
    global thread_id, room_ctr

    # Use the turnstile and lightswitch synchronization design patterns to prevent starvation
    # and allow multiple blue threads to concurrently enter the fitting room while blocking
    # green threads:
    
    #   - Once a green thread acquires the turnstile while green threads are in the fitting room,
    #     the lightswitch green_in_room will "waitlist" its entry. It is the job of the num_allowed_blue
    #     multiplexer to block its entry if the fittign room is full.
    
    #   - Once a blue thread acquires the turnstile while green threads are in the fitting room,
    #     the lightswitch green_in_room will block this thread. Therefore, the turnstile will not
    #     be released as long as this thread is blocked, effectively blocking all incoming threads
    #     and preventing starvation.
    turnstile.acquire()
    green_in_room.lock(blue_green_mutex)
    turnstile.release()

    # Following the multiplexer pattern, decrement the number of green threads that can enter the
    # fitting room. If the value of this counting semaphore drops to 0, then acquiring it will
    # block that acquiring thread.

    # As opposed to this releasing this num_allowed_green semaphore, note that acquiring it should
    # not be inside any mutex lock. Waiting on a semaphore inside a mutex lock is a well-known
    # deadlock pattern, as a thread blocking on this semaphore will prevent the mutex lock from
    # being released.
    num_allowed_green.acquire()

    # Local variable for storing the ID of the current thread
    current_thread_id = None

    # To prevent other green threads in the fitting room from interleaving and possibly resulting
    # in the IDs, counters, and display messages to be out of sync, ensure the atomicity of the
    # following sequence of operations:
    #   - Incrementing the thread ID
    #   - Incrementing the number of threads in the fitting room
    #   - Displaying the message associated with the entry of the first thread into an empty
    #     fitting room
    #   - Setting the thread ID of the current active thread
    #   - Displaying the message associated with the entry of a thread
    with room_mutex:
        thread_id += 1
        room_ctr += 1

        # Display the message associated with the entry of the first thread into an empty fitting room.
        if room_ctr == 1:
            safe_print(f"----- {GREEN} Only -----\n")

        current_thread_id = thread_id

        # Display the message associated with the entry of a thread.
        safe_print(f"Thread ID: {current_thread_id}\nColor: {GREEN}\n")

    # Simulate the stay of the green thread inside the fitting room for an arbitrary duration.
    fit_clothes()

    # To prevent other green threads in the fitting room from interleaving and possibly resulting
    # in the IDs, counters, and display messages to be out of sync, ensure the atomicity of the
    # following sequence of operations:
    #   - Incrementing the counting semaphore denoting the number of blue threads that can enter
    #     the fitting room
    #   - Decrementing the number of threads in the fitting room
    #   - Displaying the message associated with the exit of a thread
    #   - Displaying the message associated with an empty fitting room
    
    # The room_mutex lock (instead of creating a new lock) is used in order to ensure that the
    # number of threads in the fitting room is first incremented (room_ctr += 1) before it is
    # decremented (room_ctr -= 1), preventing it from assuming an illogical negative value.
    with room_mutex:
        num_allowed_green.release()
        room_ctr -= 1

        # Display the message associated with the exit of a thread.
        # This allows the user to track the threads in the fitting room.
        safe_print(f"Thread {current_thread_id} exits the fitting room.\n")

        # Display the message associated with an empty fitting room.
        if room_ctr == 0:
            safe_print(">> Empty Fitting Room\n")

    # Invoke the unlock() method of the green threads' lightswitch.
    green_in_room.unlock(blue_green_mutex)
            

# ---------------
#   MAIN THREAD
# ---------------

# Create the blue and green threads.
threads = []
for _ in range(num_blue):
    thread = threading.Thread(target = blue_thread_func)
    threads.append(thread)

for _ in range(num_green):
    thread = threading.Thread(target = green_thread_func)
    threads.append(thread)

# Shuffle the threads to randomize the order of their execution.
random.shuffle(threads)

# Start the activities of all the blue and green threads.
for thread in threads:
    thread.start()

# Block the main thread until all the blue and green threads terminate.
for thread in threads:
    thread.join()