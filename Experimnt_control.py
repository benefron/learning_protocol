import time
import random

def generate_random_number_after_delay(delay_seconds=30):
    # Wait for the specified number of seconds
    time.sleep(delay_seconds)
    
    # Generate a single random number
    random_number = random.randint(1, 100)
    print(f"Generated random number: {random_number}")
    return random_number

