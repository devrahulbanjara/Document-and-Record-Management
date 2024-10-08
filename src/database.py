import json
import os
import streamlit as st
import Levenshtein

DATABASE_PATH = "../database.json"

def load_database(file_path=DATABASE_PATH):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return None
    
    except json.JSONDecodeError as json_error:
        print(f"Error decoding JSON: {json_error}")
        return None

def is_similar(text, reference, threshold=0.8):
    similarity = 1 - (Levenshtein.distance(text, reference) / max(len(reference), len(text)))
    return similarity > threshold

def citizenship_number_exists(citizenship_number):
    database = load_database()

    if database is None:
        raise ValueError("Database loading failed. Exiting.")

    for stored_citizenship_number in database.keys():
        if is_similar(citizenship_number, stored_citizenship_number):
            if "Citizenship" in database[stored_citizenship_number]:
                print("\nCitizenship details in database: ", end=" ")
                print(database[stored_citizenship_number]["Citizenship"])
                return stored_citizenship_number, True

    print("Citizenship number not found.")
    return None, False

def normalize_name(name):
    return ' '.join(sorted(name.lower().split()))

def name_matches(name, threshold=0.7):
    database = load_database()

    if database is None:
        raise ValueError("Database loading failed. Exiting.")

    normalized_input_name = normalize_name(name)

    for details in database.values():
        stored_name = details.get('Citizenship', {}).get('name', '')
        normalized_stored_name = normalize_name(stored_name)
        
        if is_similar(normalized_input_name, normalized_stored_name, threshold=threshold):
            return True
    
    return False

def document_key_exists(citizenship_number, document_number, document_type):
    database = load_database()
    
    if document_type in database.get(citizenship_number, {}):
        print(f"{document_type} details in database: ", end=" ")
        print(database[citizenship_number][document_type])
        return True
    else:
        return False
    
def date_matches(extracted_date, extracted_citizenship_number, document_type):
    database = load_database()

    if (document_type == "Passport" or document_type == "License"):
        return extracted_date.split('-')[-1] == database[extracted_citizenship_number][document_type]["dob"].split('-')[-1]
    elif document_type == "Citizenship":
        return extracted_date == database[extracted_citizenship_number][document_type]["year_of_birth"]
   
def doc_number_matches(extracted_doc_number, citizenship_number, document_type):
    database = load_database()
    key = document_type.lower() + "_number"
    if is_similar(extracted_doc_number, database[citizenship_number][document_type][key]):
        return True
    return False

def person_info(citizenship_number,document_type):
    database=load_database()
    return database[citizenship_number][document_type]