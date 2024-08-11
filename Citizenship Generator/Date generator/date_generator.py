import csv
from datetime import date, timedelta

# Nepali digits
nepali_digits = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']

def convert_to_nepali(num):
    return ''.join(nepali_digits[int(digit)] for digit in str(num))

def generate_nepali_dates(start_year, end_year):
    current_date = date(start_year, 1, 1)
    end_date = date(end_year + 1, 1, 1)
    dates = []
    
    while current_date < end_date:
        nepali_year = convert_to_nepali(current_date.year)
        nepali_month = convert_to_nepali(f'{current_date.month:02}')
        nepali_day = convert_to_nepali(f'{current_date.day:02}')
        dates.append([nepali_year, nepali_month, nepali_day])
        current_date += timedelta(days=1)
    
    return dates

def generate_csv(filename, dates):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Month', 'Date'])
        writer.writerows(dates)

# Generate dates from Nepali year २००० to २०८१
nepali_dates = generate_nepali_dates(2000, 2081)
generate_csv('nepali_dates.csv', nepali_dates)
