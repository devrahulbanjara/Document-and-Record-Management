import re

def preprocess_text(text):
    return re.sub(r'[^A-Za-z0-9\s/-]', '', text).strip()

def filter_name(name_list):
    names = set()
    name_pattern = re.compile(
        r'(?:given\s*names?|names|name|full\s*name|cu)\s*[:/\s*-]*\s*([A-Za-z\'\-0-9\s]+)',
        re.IGNORECASE
    )
    if name_list:
        for item in name_list:
            item = preprocess_text(item)
            match = name_pattern.search(item)
            if match:
                extracted_name = match.group(1).strip()
                if extracted_name:
                    names.add(extracted_name)
    return ' '.join(names)

def filter_number(unfiltered_number):
    filtered_number = ""
    for digit in unfiltered_number:
        if digit.isdigit():
            filtered_number += digit
    return filtered_number

def filter_date(date_str):
    month_map = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
        'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
        'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }
    match = re.search(r'(\d{1,2})\s*([A-Z]{3})\s*(\d{4})', date_str)
    if match:
        day = match.group(1).zfill(2)
        month_text = match.group(2).upper()
        year = match.group(3)
        month = month_map.get(month_text, '')
        return f"{day}-{month}-{year}"
    return ''

def filter_surname(surname_list):
    surnames = set()
    surname_pattern = re.compile(
        r'(?:surnam|surna|sumame|sumame|/surname|r\s*surname|rsurname)\s*[:/\s*-]*\s*([A-Za-z\'\-0-9\s]+)',
        re.IGNORECASE
    )
    if surname_list:
        for item in surname_list:
            item = preprocess_text(item)
            match = surname_pattern.search(item)
            if match:
                extracted_surname = match.group(1).strip()
                if extracted_surname:
                    surnames.add(extracted_surname)
    return ' '.join(surnames)

def filter_passport_details(collected_texts):
    extracted_texts = {}
    for label, texts in collected_texts.items():
        filtered_values = []
        for text in texts:
            text = preprocess_text(text)
            if label == 'dob':
                filtered_value = filter_date(text)
                if filtered_value:
                    filtered_values.append(filtered_value)
            elif label == 'name':
                filtered_value = filter_name([text])
                filtered_values.append(filtered_value)
            elif label == 'surname':
                filtered_value = filter_surname([text])
                filtered_values.append(filtered_value)
            else:
                filtered_value = filter_number(text)
                filtered_values.append(filtered_value)
        if filtered_values:
            if label in ['citizenship_number', 'contact_number', "license_number"]:
                extracted_texts[label] = " ".join(filtered_values).replace(" ", "")
            else:
                extracted_texts[label] = " ".join(filtered_values)
        else:
            extracted_texts[label] = ""
    return extracted_texts
