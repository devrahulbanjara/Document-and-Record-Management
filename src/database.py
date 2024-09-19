import json
import streamlit as st

database="database.json"    
def insert_passport(name,surname,dob,citizenship_number,passport_number):
    
    new_passport_details = {
        "name" : name,
        "surname" : surname,
        "dob" : dob,
        "citizenship_number" : citizenship_number,
        "passport_number" : passport_number
        }
    
    with open(database,"r") as f:
        data=json.load(f)
    
    if citizenship_number in data:
        print("The person with citizenship number exists in the database.")

        if "Passport" not in data[citizenship_number]:
            data[citizenship_number]["Passport"] = new_passport_details
            print("Inserted Passport details.")
        # st.write("The person with citizenship number exists in the database.")
        else:
            print("The person with citizenship number already has passport details.")
            
    else:
        # st.warning("The person with citizenship number does not exist in the database.")
        print("The person with citizenship number does not exist in the database.")
        
    with open(database,"w") as f:
        json.dump(data,f,indent=4)
