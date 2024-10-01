import streamlit as st

def plot_citizenship(details, is_genuine):
    st.markdown("<h4 class='subtitle' style='text-align: center; color: #4B0082;'>Extracted Information</h4>", unsafe_allow_html=True)
    birth_place = details.get('birth_place', 'Unknown') if is_genuine==True else details.get('district', 'Unknown')
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>नाम:</strong> {details.get('name', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>जन्मस्थान:</strong> {birth_place}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>जन्म साल:</strong> {details.get('year_of_birth', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>लिङ्ग:</strong> {details.get('gender', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>नागरिकता नम्बर:</strong> {details.get('citizenship_number', 'Unknown')}</p>", unsafe_allow_html=True)

def plot_license(details):
    st.markdown("<h4 class='subtitle' style='text-align: center; color: #4B0082;'>Extracted Information</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>Name:</strong> {details['name'].title()}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>DOB:</strong> {details.get('dob', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>Contact Number:</strong> {details.get('contact_number', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>Citizenship Number:</strong> {details.get('citizenship_number', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>License Number:</strong> {details.get('license_number', 'Unknown')}</p>", unsafe_allow_html=True)

def plot_passport(details):
    st.markdown("<h4 class='subtitle' style='text-align: center; color: #4B0082;'>Extracted Information</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>Name:</strong> {details['name'].title()}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>Surname:</strong> {details.get('surname', 'Unknown').title()}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>DOB:</strong> {details.get('dob', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>Citizenship Number:</strong> {details.get('citizenship_number', 'Unknown')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; text-align: center;'><strong>Passport Number:</strong> {details.get('passport_number', 'Unknown')}</p>", unsafe_allow_html=True)


