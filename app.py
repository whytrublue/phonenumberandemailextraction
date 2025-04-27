import streamlit as st
import pandas as pd
import re

# Function to extract phone numbers, names, and email addresses from the text
def extract_contact_details(text):
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

    # Return extracted details as a list of dictionaries
    extracted_data = []
    for email, phone in zip(email_addresses, phone_numbers):
        extracted_data.append({
            "Email": email,
            "Phone 1": phone,  # You can customize if you want to separate phones
            "Phone 2": None  # Placeholder for a second phone number if you need to extract more
        })
    return extracted_data

# Streamlit app interface
def main():
    st.title("Information Extractor")

    # File upload and text input options
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    st.write("OR")
    text_input = st.text_area("Paste your text here:", height=200)

    # Process the input when the button is pressed
    if st.button("Extract"):
        if uploaded_file is not None:
            # Read the uploaded file
            text = uploaded_file.read().decode('utf-8')
        elif text_input:
            # Use pasted text if no file uploaded
            text = text_input
        else:
            st.error("Please upload a file or paste some text.")
            st.stop()

        # Extract contact details
        extracted_data = extract_contact_details(text)
        
        if not extracted_data:
            st.warning("No emails or phone numbers found.")
            st.stop()
        
        # Create a DataFrame from the extracted data
        df = pd.DataFrame(extracted_data)
        
        # Display the results
        st.subheader("Extracted Data")
        st.dataframe(df)
        
        # Format for copy-paste
        formatted_data = "\n".join(
            f"{row['Email']}\t{row['Phone 1'] or 'None'}\t{row['Phone 2'] or 'None'}"
            for _, row in df.iterrows()
        )
        
        st.subheader("📋 Copy-Paste Format")
        st.code(formatted_data)
        
        # Provide an option to download the results as a CSV file
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download as CSV",
            data=csv,
            file_name="contacts.csv",
            mime="text/csv"
        )

# Run the Streamlit app
if __name__ == "__main__":
    main()
