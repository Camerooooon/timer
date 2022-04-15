import time

class Timer:
    start_time: int
    end_time: int
    alerted_expired: bool
    
    def __init__(self, start_time, end_time, alerted_expired):
        self.start_time = start_time
        self.end_time = end_time
        self.alerted_expired = alerted_expired

    def expired(self) -> bool:
        return time.time() > self.end_time

    def time_left(self) -> int:
        if self.expired():
            return 0
        return self.end_time - time.time()

    def mod_duration(self, mod: int):
        self.end_time = self.end_time + mod
   
    def serialise(self) -> str:
        '''
        Transports the class into a format savable to a file

            Returns:
                serialization (str): simple object form
        '''
        
        # The reason for multiply by 1000 is to get rid of the decimal point for storage and parsing later and then round get rid of all the decimals
        return str(round(self.start_time*1000)) + " " + str(round(self.end_time*1000)) + " " + str(self.alerted_expired)

def from_duration(duration: int) -> Timer:
    '''
    Creates a new instance of a Timer
    
        Parameters:
            duration (int): the length of the timer in seconds
    
    '''
    
    start_time = time.time()
    end_time = time.time() + duration
    return Timer(start_time, end_time, False)

def from_serialization(data: str) -> Timer:
    '''
    Creates a new instance of a Timer from a string
    
        Parameters:
            serialization (str): the saved data about the timer
    
    '''
    start_data, end_data, alerted_expired_ = data.split(" ")
    start_time = int(start_data)/1000
    end_time = int(end_data)/1000
    alerted_expired = alerted_expired_ in "True"
    return Timer(start_time, end_time, alerted_expired)
