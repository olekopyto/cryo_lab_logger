from datetime import datetime

def get_formatted_date_time():
    now = datetime.now()
    formatted_date_time = now.strftime("%d/%H:%M:%S")
    return formatted_date_time

# Example usage:
formatted_date_time = get_formatted_date_time()
print(formatted_date_time)