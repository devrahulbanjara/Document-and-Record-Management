import json
import os
import streamlit as st

def load_database(file_path):
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

def is_similar(text, reference):
    matches = sum(1 for t_char, r_char in zip(text, reference) if t_char == r_char)
    return matches / max(len(reference), len(text)) > 0.8

def citizenship_number_exists(citizenship_number, database_path="database.json"):
    database = load_database(database_path)

    if database is None:
        raise ValueError("Database loading failed. Exiting.")

    for stored_citizenship_number in database.keys():
        if is_similar(citizenship_number, stored_citizenship_number):
            if "Citizenship" in database[stored_citizenship_number]:
                print("Citizenship details in database: ", end=" ")
                print(database[stored_citizenship_number]["Citizenship"])
                return True
            else:
                print(f"\n Key 'Citizenship' not found for {stored_citizenship_number}")
                return False


def name_matches(name, database_path="database.json"):
    database = load_database(database_path)

    if database is None:
        raise ValueError("Database loading failed. Exiting.")

    for details in database.values():
        stored_name = details.get('Citizenship', {}).get('name', '')
        if is_similar(name, stored_name):
            return True
    
    return False

def document_key_exists(citizenship_number, document_number, document_type, database_path="database.json"):
    database = load_database(database_path)
    
    if document_type in database.get(citizenship_number, {}):
        print(f"{document_type} details in database: ",end=" ")
        print(database[citizenship_number][document_type])
        return True
    else:
        return False
    
def date_matches(extracted_date, extracted_citizenship_number, document_type, compare_with=None, database_path="database.json"):
    database = load_database(database_path)
    if (document_type == "Passport" or document_type == "License") and compare_with:
        return extracted_date.split('-')[-1] == database[extracted_citizenship_number]["Citizenship"]["year_of_birth"]
    elif (document_type == "Passport" or document_type == "License") and compare_with is None:
        return extracted_date.split('-')[-1] == database[extracted_citizenship_number][document_type]["dob"].split('-')[-1]
    elif document_type == "Citizenship":
        return extracted_date == database[extracted_citizenship_number][document_type]["year_of_birth"]
   
def doc_number_matches(extracted_doc_number, citizenship_number, document_type, database_path="database.json"):
    database = load_database(database_path)
    key = document_type.lower() + "_number"
    if is_similar(extracted_doc_number, database[citizenship_number][document_type][key]):
        return True
    return False
