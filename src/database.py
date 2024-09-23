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

def check_citizenship_number(citizenship_number, name,database_path="database.json"):
    database = load_database(database_path)
    
    if database is None:
        raise ValueError("Database loading failed. Exiting.")
        st.stop()

    for stored_citizenship_number, details in database.items():
        if is_similar(citizenship_number, stored_citizenship_number):
            stored_name = details.get('Citizenship', {}).get('name', '')
            if is_similar(name, stored_name):
                return True
    
    return False

def check_document(citizenship_number, document_number, document_type, database_path="database.json"):
    database = load_database(database_path)
    
    if document_type in database.get(citizenship_number, {}):
        document_key = document_type.lower() + "_number"
        if is_similar(database[citizenship_number][document_type][document_key], document_number):
            st.warning(f"The {document_type} exists in the database.")
        else:
            st.warning(f"{document_type} number doesn't match with the one in the database.")
    else:
        st.warning(f"The {document_type} under the given citizenship number doesn't exist in the database.")
    
