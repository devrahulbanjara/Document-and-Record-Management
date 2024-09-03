import csv
from datetime import date, timedelta

# Nepali digits
nepali_digits = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']

def convert_to_nepali(num):
    return ''.join(nepali_digits[int(digit)] for digit in str(num))

def generate_nepali_dates(start_year, end_year, total_rows):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    total_days = (end_date - start_date).days
    step = max(total_days // total_rows, 1)  # Calculate step to distribute dates

    dates = []
    for i in range(total_rows):
        current_date = start_date + timedelta(days=i * step)
        nepali_year = convert_to_nepali(current_date.year)
        nepali_month = convert_to_nepali(f'{current_date.month:02}')
        nepali_day = convert_to_nepali(f'{current_date.day:02}')
        dates.append([nepali_year, nepali_month, nepali_day])
    
    return dates

def generate_csv(filename, dates):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Month', 'Date'])
        writer.writerows(dates)

# Generate 800 rows of dates from Nepali year २००१ to २०८०
nepali_dates = generate_nepali_dates(2001, 2080, 800)
generate_csv('nepali_dates.csv', nepali_dates)
