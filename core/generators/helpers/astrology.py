
from datetime import datetime



def get_element(datestamp):
    sign = get_sun_sign_from_current_date(datestamp)
    return _sign_to_elements(sign)


def get_sun_sign_from_current_date(datestamp):
    month = datestamp.month
    day = datestamp.day


    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return 'aries'
    elif(month == 4 and day >= 20) or (month == 5 and day <=20):
        return 'taurus'
    elif(month == 5 and day >= 21) or (month == 6 and day <=20):
        return 'gemini'
    elif(month == 6 and day >= 21) or (month == 7 and day <=22):
        return 'cancer'   
    elif(month == 7 and day >= 23) or (month == 8 and day <=22):
        return 'leo'
    elif(month == 8 and day >= 23) or (month == 9 and day <=22):
        return 'virgo'   
    elif(month == 9 and day >= 23) or (month == 10 and day <=22):
        return 'libra'
    elif(month == 10 and day >= 23) or (month == 11 and day <=21):
        return 'scorpio'   
    elif(month == 11 and day >= 22) or (month == 12 and day <=21):
        return 'sagittarius'   
    elif(month == 12 and day >= 22) or (month == 1 and day <=19):
        return 'capricon'   
    elif(month == 1 and day >= 20) or (month == 2 and day <=18):
        return 'aquarius'   
    elif(month == 2 and day >= 19) or (month == 3 and day <=20):
        return 'pisces'   
    else:
        return "unknown"



def _sign_to_elements(sign):
    FIRE = ["aries", "leo","sagittarius"]
    WATER = ["pisces","scorpio","cancer"]
    AIR = ["gemini" , "libra" , "aquarius"]
    EARTH =["virgo","taurus","capricorn"] 



    if sign in FIRE: return "fire"
    if sign in WATER: return "water"
    if sign in AIR: return "air"
    if sign in EARTH: return "earth"

    else :
        return "unknown"
