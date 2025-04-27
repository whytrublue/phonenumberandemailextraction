import streamlit as st
import re
import pandas as pd

def extract_contact_details(text):
    # Regex patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    # Split into contact blocks (separated by empty lines)
    contact_blocks = re.split(r'\n\s*\n', text.strip())
    
    contacts = []
    
    for block in contact_blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue
            
        email = None
        phones = []
        
        for line in lines:
            # Check for email
            email_match = re.search(email_pattern, line)
            if email_match:
                email = email_match.group(0)
            
            # Check for phone numbers
            phone_matches = re.findall(phone_pattern, line)
            phones.extend(phone_matches)
        
        if email:
            contacts.append({
                "Email": email,
                "Phone 1": phones[0] if len(phones) > 0 else None,
                "Phone 2": phones[1] if len(phones) > 1 else None
            })
    
    return contacts

# Streamlit app
st.title("Email & Phone Extractor 📄📞")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
st.write("OR")
text_input = st.text_area("Paste your text here:", height=200)

if st.button("Extract"):
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    elif text_input:
        text = text_input
    else:
        st.error("Please upload a file or paste some text.")
        st.stop()

    extracted_data = extract_contact_details(text)
    
    if not extracted_data:
        st.warning("No emails or phone numbers found.")
        st.stop()
    
    # Create DataFrame
    df = pd.DataFrame(extracted_data)
    
    # Display results
    st.subheader("Extracted Data")
    st.dataframe(df)
    
    # Format for copy-paste
    formatted_data = "\n".join(
        f"{row['Email']}\t{row['Phone 1'] or 'None'}\t{row['Phone 2'] or 'None'}"
        for _, row in df.iterrows()
    )
    
    st.subheader("📋 Copy-Paste Format")
    st.code(formatted_data)
    
    # Download options
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download as CSV",
        data=csv,
        file_name="contacts.csv",
        mime="text/csv"
    )
