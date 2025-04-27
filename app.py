import streamlit as st
import re
import pandas as pd

def extract_contact_details(text):
    # First normalize all whitespace and line breaks
    text = re.sub(r'\s+', ' ', text)  # Replace any whitespace with single space
    text = re.sub(r' ?Email: ?', '\nEmail: ', text)  # Normalize email prefix
    text = re.sub(r' ?Cell: ?', '\nCell: ', text)  # Normalize cell prefix
    
    # Split into contact blocks (separated by Email: or Cell: patterns)
    blocks = re.split(r'(?:Email:|Cell:)\s*', text)
    blocks = [block.strip() for block in blocks if block.strip()]
    
    contacts = []
    current_email = None
    current_phones = []
    
    for block in blocks:
        # Check if block contains an email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', block)
        if email_match:
            # If we already have an email, save the current contact
            if current_email:
                contacts.append({
                    "Email": current_email,
                    "Phone 1": current_phones[0] if len(current_phones) > 0 else None,
                    "Phone 2": current_phones[1] if len(current_phones) > 1 else None
                })
                current_phones = []
            current_email = email_match.group(0)
        
        # Extract phone numbers from block
        phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', block)
        current_phones.extend(phones)
    
    # Add the last contact
    if current_email:
        contacts.append({
            "Email": current_email,
            "Phone 1": current_phones[0] if len(current_phones) > 0 else None,
            "Phone 2": current_phones[1] if len(current_phones) > 1 else None
        })
    
    return contacts

# Streamlit UI
st.title("Contact Info Extractor")

input_text = st.text_area("Paste contact information:", height=300)

if st.button("Extract"):
    if not input_text.strip():
        st.warning("Please paste some contact information")
    else:
        contacts = extract_contact_details(input_text)
        
        if not contacts:
            st.warning("No contact information found")
        else:
            # Create DataFrame
            df = pd.DataFrame(contacts)
            
            # Display results
            st.write("### Extracted Contacts")
            st.dataframe(df)
            
            # Create TSV output
            tsv_output = "\n".join(
                f"{row['Email']}\t{row['Phone 1'] or 'None'}\t{row['Phone 2'] or 'None'}"
                for _, row in df.iterrows()
            )
            
            st.download_button(
                "Download as TSV",
                data=tsv_output,
                file_name="contacts.tsv",
                mime="text/tsv"
            )
