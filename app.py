import streamlit as st
import pandas as pd
import re

# Function to extract contacts (customize this to your needs)
def extract_contacts(text, separator):
    # Example: extracting emails, mobile, and office numbers using regex (you can modify this)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})'

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    # Mocking data for demonstration
    extracted_data = []
    for i in range(min(len(emails), len(phones))):
        extracted_data.append({
            "Email": emails[i],
            "Mobile": phones[i],
            "Office": phones[i]  # You can modify this to have a separate office phone number if needed
        })
    
    return extracted_data

# Streamlit app
st.title("Extract Emails, Mobile, and Office Numbers 📄📞")

uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type=["txt"])

st.write("OR")

text_input = st.text_area("Paste your text here:")

# --- Separator Input ---
separator_input = st.text_input("✂️ Enter a custom separator between contacts (e.g., READ MORE, -----, ###)")

if st.button("Extract"):
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    elif text_input:
        text = text_input
    else:
        st.error("Please upload a file or paste some text.")
        st.stop()

    # Pass the custom separator as an argument to the extraction function
    extracted_data = extract_contacts(text, separator_input)
    df = pd.DataFrame(extracted_data)

    # Display results as a table
    st.subheader("Extracted Data Table")
    st.dataframe(df)  # This will show the data in a table format

    # Format the extracted data for copy-pasting with custom separator
    formatted_data = separator_input.join(df.apply(lambda row: "\t".join(row.astype(str)), axis=1))

    # Display the formatted data with a copy option
    st.subheader("📋 Copy Extracted Data")
    st.code(formatted_data, language="text")

    # Option to download the extracted data as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Extracted Data as CSV",
        data=csv,
        file_name="extracted_contacts.csv",
        mime='text/csv'
    )
