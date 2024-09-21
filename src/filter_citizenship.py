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

def filter_number(ulfiltered_number):
    english_number = ""

    for digit in ulfiltered_number:
        if digit in nepali_to_english_mapping.keys():
            english_number += nepali_to_english_mapping[digit]

    return english_number

def filter_text(unfiltered_text):
    unwanted = [
        '।', '॥', '|', '-', '.', ',', '?', '!', '(', ')', '[', ']', '{', '}', ':', ';', 
        '_', '*', '#', '@', '&', '%', '$', 
        '०', '१', '२', '३', '४', '५', '६', '७', '८', '९'
    ]

    filtered_text = ""
    for alphabet in unfiltered_text:
        if alphabet not in unwanted:
            filtered_text += alphabet

    return filtered_text.split()

# print(filter_number("ना.प्रननं. २५-०१-७९-०२७३८"))  # Output: 25-01-79-02738
print(filter_text("जिल्ला : नुवाकोट"))  # Output: "ना प्रननं  जिल्ला  नुवाकोट"



#text ko cast ma filter text function ma pass garera list ma output dinxa tesko [1:]