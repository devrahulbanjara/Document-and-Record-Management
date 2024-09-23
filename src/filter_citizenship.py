nepali_to_english_mapping = {
    "०": "0",
    "१": "1",
    "२": "2",
    "३": "3",
    "४": "4",
    "५": "5",
    "६": "6",
    "७": "7",
    "८": "8",
    "९": "9"
}

def filter_number(unfiltered_number):
    english_number = ""

    for digit in unfiltered_number:
        if digit in nepali_to_english_mapping.keys():
            english_number += nepali_to_english_mapping[digit]

    return english_number

def filter_text(unfiltered_text):
    unwanted = [
        '।', '॥', '|', '-', '.', ',', '?', '!', '(', ')', '[', ']', '{', '}', ':', ';', 
        '_', '*', '#', '@', '&', '%', '$', 
        '०', '१', '२', '३', '४', '५', '६', '७', '८', '९',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        '~', '`', '+', '=', '<', '>', '\\', '"', "'", ';', '¬', '^', '°', '§', '¤', '©', '®', 
        '¥', '¢', '£', '€', '•', '-', '—', '…', '«', '»', '<', '>'
    ]

    filtered_text = ""
    for alphabet in unfiltered_text:
        if alphabet not in unwanted:
            filtered_text += alphabet

    return filtered_text.split()

def filter_citizenship_details(collected_texts):
    male = "पुरुष"
    female = "महिला"
    others = "अन्य"

    def is_similar(text, reference):
        return sum(1 for char in reference if char in text) / len(reference) > 0.6

    extracted_texts = {}
    name_concat = ""

    for label, texts in collected_texts.items():
        filtered_values = []
        gender_found = False

        for text in texts:
            if label == 'citizenship_number' or label == 'year':
                filtered_value = filter_number(text)
                if filtered_value:
                    filtered_values.append(filtered_value)

            elif label == 'gender':
                if gender_found:
                    break
                if is_similar(text, female):
                    gender = "महिला"
                    gender_found = True
                elif is_similar(text, male):
                    gender = "पुरुष"
                    gender_found = True
                elif is_similar(text, others):
                    gender = "अन्य"
                    gender_found = True
                filtered_values.append(gender)
                break

            elif label == "district":
                filtered_text = filter_text(text)
                for word in filtered_text:
                    if "ज" in word and "ल" in word:
                        continue
                    filtered_values.append(word)

            elif label == "name":
                filtered_text = filter_text(text)
                for word in filtered_text:
                    if "नाम" in word or "थर" in word:
                        continue
                    filtered_values.append(word)

        if filtered_values:
            if label in ['citizenship_number', 'year']:
                extracted_texts[label] = " ".join(filtered_values).replace(" ", "")
            else:
                extracted_texts[label] = " ".join(filtered_values)
        else:
            extracted_texts[label] = ""

    return extracted_texts