def find_highest_number(numbers):
    highest = 0
    for number in numbers:
        if number > highest:
            highest = number
    return highest

def calculate_days_between_dates(from_date, to_date):
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")
    return abs((to_date - from_date).days)

# find all images without alternative text
# and give them a reasonable alternative text
