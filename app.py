import re
import streamlit as st

def extract_contact_info(text):
    # Extract all email addresses
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    
    # Extract all phone numbers (standard US formats)
    phone_numbers = re.findall(r'\(?\d{3}\)?[-\.\s]?\d{3}[-\.\s]?\d{4}', text)
    # Clean phone numbers (keep only digits and hyphens)
    phone_numbers = [re.sub(r'[^\d-]', '', num) for num in phone_numbers]
    
    # Pair them up (simple approach - assumes order matches)
    contacts = []
    max_length = max(len(emails), len(phone_numbers))
    
    for i in range(max_length):
        email = emails[i] if i < len(emails) else None
        phone = phone_numbers[i] if i < len(phone_numbers) else None
        contacts.append((email, phone))
    
    return contacts

def main():
    st.title("Email & Phone Extractor")
    
    input_text = st.text_area("Paste any text containing emails and phone numbers:", height=300)
    
    if st.button("Extract Information"):
        if input_text.strip():
            contacts = extract_contact_info(input_text)
            
            if contacts:
                st.success(f"Found {len(contacts)} contacts!")
                st.write("### Extracted Data")
                
                # Prepare output
                output = []
                for email, phone in contacts:
                    output.append(f"{email or 'None'}\t{phone or 'None'}")
                
                # Display results
                st.text_area("Results:", "\n".join(output), height=300)
                
                # Download button
                st.download_button(
                    label="Download as TSV",
                    data="\n".join(output),
                    file_name="extracted_contacts.tsv",
                    mime="text/tsv"
                )
            else:
                st.warning("No emails or phone numbers found.")
        else:
            st.warning("Please paste some text first.")

if __name__ == "__main__":
    main()
