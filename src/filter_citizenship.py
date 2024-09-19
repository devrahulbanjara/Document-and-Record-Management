

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

english_filtered_citizenship_number = ""

for digit in nepali_filtered_citizenship_number:
    english_filtered_citizenship_number += nepali_to_english_mapping[digit]