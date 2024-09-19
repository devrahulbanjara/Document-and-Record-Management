import json
import os

database = "database.json"

def read_database():
    if not os.path.exists(database):
        return {}
    try:
        with open(database, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error decoding JSON from the database file. Returning empty data.")
        return {}
    except Exception as e:
        print(f"Error reading database: {e}")
        return {}

def write_database(data):
    try:
        with open(database, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing to database: {e}")

def update_database(citizenship_number, document_data, document_type):
    data = read_database()
    
    if citizenship_number not in data:
        data[citizenship_number] = {}
    
    data[citizenship_number][document_type] = document_data
    
    write_database(data)
    print(f"Successfully inserted {document_type} into the database with citizenship number {citizenship_number}")

def insert_passport(name, surname, dob, citizenship_number, passport_number):
    new_passport_details = {
        "name": name,
        "surname": surname,
        "dob": dob,
        "citizenship_number": citizenship_number,
        "passport_number": passport_number
    }
    update_database(citizenship_number, new_passport_details, "Passport")

def insert_license(name, contact_number, dob, citizenship_number, license_number):
    new_license_details = {
        "name": name,
        "contact_number": contact_number,
        "dob": dob,
        "citizenship_number": citizenship_number,
        "license_number": license_number
    }
    update_database(citizenship_number, new_license_details, "License")

def insert_citizenship(name, district, dob, citizenship_number, gender):
    new_citizenship_details = {
        "name": name,
        "district": district,
        "dob": dob,
        "citizenship_number": citizenship_number,
        "gender": gender
    }
    update_database(citizenship_number, new_citizenship_details, "Citizenship")

def citizenship_exists(citizenship_number):
    data = read_database()
    return citizenship_number in data

def doc_info_exists(document_type, citizenship_number):
    data = read_database()
    return document_type in data.get(citizenship_number, {})
