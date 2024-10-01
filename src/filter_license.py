import re

def filter_number(unfiltered_number):
    filtered_number = ""

    for digit in unfiltered_number:
        if digit.isdigit():
            filtered_number += digit

    return filtered_number

def filter_date(unfiltered_date):
    filtered_date = ""
    for i in unfiltered_date:
        if i.isdigit() or i == "-":
            filtered_date+=i
    return filtered_date

def filter_name(name_list):
    names = set()

    name_pattern = re.compile(
        r'\b(?:name|nam|na|n|ame)\s*[:\s*-]*\s*([A-Za-z\s\'\-0-9]*)',
        re.IGNORECASE
    )

    if name_list:
        for item in name_list:
            match = name_pattern.search(item)
            if match:
                extracted_name = match.group(1).strip()
                if extracted_name:
                    names.add(extracted_name)

    return ' '.join(names)

def filter_license_details(collected_texts):
    extracted_texts = {}

    for label, texts in collected_texts.items():
        filtered_values = []

        for text in texts:
            if label == 'dob':
                filtered_value = filter_date(text)
                if filtered_value:
                    filtered_values.append(filtered_value)

            elif label == 'name':
                filtered_value = filter_name([text])
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
