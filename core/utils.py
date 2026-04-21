


import random
import time







def weighted_pick(options):

    random.seed(time.time())#ensures each call is unique 
    random_index = random.randint(0,len(options) -1 )
    
    return options[random_index]

