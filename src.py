import threading, time, sys

DEBUG = False

def input_with_timout(timeout_secs: float, prompt: str = "", max_polling_secs: float = 0.51) -> str | None:
    '''
    Get input from console with a timeout, defined by the 'timeout_secs' parameter.
    The more accurate the 'timeout_secs'parameter is, the more frequent polling may likely be (may hinder performance if too frequent). 
    Returns None if timed out
    
    timeout_secs: How many seconds to wait before raising timeout exception.
    prompt: Print text before taking input, just like standard input(). Defaults to None.

    Max accuracy is 4 decimal points, this is written in pure python so performance hit is bad with high accuracies!
    '''
    global uinput, max_factor
    uinput = None
    decrement_step = 1
    max_factor = max_polling_secs
    max_accuracy = 4

    #measure dps (decimal places)
    def GetNumberOfDecimalPlaces() -> int:
        timeout= str(timeout_secs)
        if timeout.find('.') == -1:
            return 0
        timeout = timeout[timeout.index('.')+1:]
        if DEBUG:
            print(f"Found {len(timeout)} decimal places")
        return len(timeout)
    #get highest factor within max factor threshold
    def GetHighestStep() -> float:
        global max_factor
        timeout_int = int(timeout_secs * zero_dp)
        max_factor *= zero_dp
        highest_factor = 0
        for i in range(1, timeout_int + 1):
           if timeout_int  % i == 0:
               
               if max_factor < i: #factor above max factor threshold then stop
                   break
               highest_factor = i
        if DEBUG:
            print(f"Highest factor: {highest_factor}")
            #print(f"Max factor: {max_factor}")
        return highest_factor / zero_dp 
    def InputFunc():
        global uinput
        uinput = input(prompt)
        sys.exit(0) #close thread

    dp = GetNumberOfDecimalPlaces()
    zero_dp: int
    if dp > 0:
        temp1 = "1"
        for _ in range(0, dp):
            temp1 += "0"
        zero_dp = int(temp1)
        decrement_step /= zero_dp
        if DEBUG:
            print(f"Based on decimal places found, zero_dp: {zero_dp}")
        
        #set decrement step to highest factor
        decrement_step = GetHighestStep()
    
    if DEBUG:
        print(f"Highest step found within {max_factor / zero_dp}s factor threshold is: {decrement_step}")
    #
    
    #make and start thread
    if DEBUG:
        print(f"Starting thread")
    thread = threading.Thread(target=InputFunc)
    thread.start()
    if DEBUG:
        print(f"Waiting... {timeout_secs} seconds")
    #wait and decrement timeout by 1 every mi until timeout reaches 0
    while timeout_secs != 0 and uinput == None:
        time.sleep(decrement_step)
        timeout_secs -= decrement_step
        timeout_secs = round(timeout_secs, max_accuracy)
        #print(timeout_secs)
    
    if DEBUG:
        if uinput == None:
            print("NO INPUT GIVEN! TIME OUT!")
        else:
            print("INPUT GIVEN! " + uinput)

    return uinput

