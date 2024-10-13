
def check_quality(status_code, total_time):
    match status_code:
        case 200:
            if(total_time > 3):
                return "Terrible"
            if(total_time > 2):
                return "Very Bad"
            if(total_time > 1):
                return "Bad"
            if(total_time < 1 and total_time > 0.7):
                return "Good"
            if(total_time < 0.7 and total_time > 0.5):
                return "Very Good"
            if(total_time < 0.5 and total_time > 0.3):
                return "Excellent"
            if(total_time < 0.3):
                return "Amazing"              
        case 400:
            return "Client Error"
        case 500:
            return "Server Error"
        case _:
            return "Unknown Status Code"