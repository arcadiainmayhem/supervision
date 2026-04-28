


#sum it down to single digit
def reduce(number):
    while number > 9:
        total = 0 #resets each iteration
        for d in str(number):
            total += int(d)
        number = total
    return number


def calculate(visitor_data ):
    number = visitor_data["visitor_number"]


    visitor_datestamp = visitor_data["datestamp"]

    day = visitor_datestamp.day
    hour = visitor_datestamp.hour
    month= visitor_datestamp.month
    year = visitor_datestamp.year



    combined = number + day + hour + month + year


    return reduce(combined) 