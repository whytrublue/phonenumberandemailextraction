import streamlit as st
import re

# Function to extract phone numbers, names, and email addresses from the text
def extract_info(text):
    # Define regular expressions for phone numbers, email addresses, and names
    phone_patterns = [
        r"\+?(\d{1,3})?[\s.-]?\(?(\d{1,4})\)?[\s.-]?(\d{1,4})[\s.-]?(\d{1,4})",  # International or local phone formats
        r"\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})",  # 123-456-7890 format
        r"\+?(\d{10,15})"  # Catch phone numbers with country code and no separators
    ]
    
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    
    # Extract phone numbers
    phone_numbers = []
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            phone_number = ''.join(match).strip()
            phone_numbers.append(phone_number)
    
    # Extract email addresses
    email_addresses = re.findall(email_pattern, text)
    
    # Extract names (assuming the format is "First Last" or "First Middle Last")
    name_pattern = r"([A-Za-z]+(?: [A-Za-z]+){1,2})"  # Match first name, middle name, and last name
    names = re.findall(name_pattern, text)

    # Handle multi-line cases by checking each line separately
    lines = text.split('\n')
    phone_numbers_multiline = []
    email_addresses_multiline = []
    names_multiline = []

    for line in lines:
        # Check for phone numbers
        for pattern in phone_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                phone_number = ''.join(match).strip()
                phone_numbers_multiline.append(phone_number)

        # Check for email addresses
        email_matches = re.findall(email_pattern, line)
        email_addresses_multiline.extend(email_matches)

        # Check for names
        name_matches = re.findall(name_pattern, line)
        names_multiline.extend(name_matches)

    # Remove duplicates by converting lists to sets
    phone_numbers = list(set(phone_numbers + phone_numbers_multiline))
    email_addresses = list(set(email_addresses + email_addresses_multiline))
    names = list(set(names + names_multiline))

    return phone_numbers, email_addresses, names

# Streamlit app interface
def main():
    st.title("Information Extractor")

    # Text input area
    text_input = st.text_area("Enter text with phone numbers, names, and email addresses:")

    if text_input:
        # Extract phone numbers, email addresses, and names
        phone_numbers, email_addresses, names = extract_info(text_input)

        # Display extracted information
        if phone_numbers:
            st.subheader("Extracted Phone Numbers:")
            for number in phone_numbers:
                st.write(number)
        else:
            st.write("No phone numbers found.")
        
        if email_addresses:
            st.subheader("Extracted Email Addresses:")
            for email in email_addresses:
                st.write(email)
        else:
            st.write("No email addresses found.")
        
        if names:
            st.subheader("Extracted Names:")
            for name in names:
                st.write(name)
        else:
            st.write("No names found.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
