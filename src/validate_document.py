import streamlit as st
from database import citizenship_number_exists, document_key_exists, doc_number_matches, date_matches

def validate_document(details, document_type, document_number_key):
    stored_citizenship_number, number_exists = citizenship_number_exists(details["citizenship_number"])
    
    is_genuine = False
    if number_exists:
        if document_key_exists(stored_citizenship_number, details[document_number_key], document_type):
            if doc_number_matches(details[document_number_key], stored_citizenship_number, document_type):
                if date_matches(details["dob"], stored_citizenship_number, document_type):
                    is_genuine = True
                    details["citizenship_number"] = stored_citizenship_number
                    return is_genuine
                else:
                    return f"❌ The extracted {document_type} DOB doesn't match with the {document_type} DOB in the JSON."
            else:
                return f"❌ The {document_type} number does not match the one in the database."
        else:
            return f"❌ The given person has no {document_type.lower()} registered."
    else:
        return f"❌ The citizenship number which is in the {document_type} doesn't exist."