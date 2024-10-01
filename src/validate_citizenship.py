import streamlit as st
from database import citizenship_number_exists, date_matches, name_matches

def validate_citizenship(details):
    stored_citizenship_number, number_exists = citizenship_number_exists(details["citizenship_number"])
    is_genuine = False
    if number_exists:
        if date_matches(details["year_of_birth"], stored_citizenship_number, "Citizenship"):
            if name_matches(details["name"]):
                is_genuine = True
                details["citizenship_number"] = stored_citizenship_number
                return is_genuine
            else:
                return "❌ Citizenship number exists, but the name doesn't match."
        else:
            return "❌ Citizenship number exists, but the date doesn't match."
    else:
        return "❌ The given citizenship number doesn't exist."