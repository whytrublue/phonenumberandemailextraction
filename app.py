import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'

    # Keywords
    mobile_keywords = ['c', 'm', 'mobile', 'cell', 'cellphone']

    # Extract all emails
    emails = re.findall(email_pattern, text)

    # Split text into blocks
    blocks = text.splitlines()

    results = []
    email_index = 0

    i = 0
    while i < len(blocks):
        block = blocks[i].strip()

        if re.match(email_pattern, block):
            email = block
            mobile = None
            office = None

            if i + 1 < len(blocks):
                next_block = blocks[i + 1].strip()

                # Find phones in next line
                phones = re.findall(phone_pattern, next_block)

                # Prioritize mobile by keywords
                if 'c:' in next_block.lower() or 'm:' in next_block.lower() or 'mobile' in next_block.lower():
                    mobile_search = re.search(r'(?:c|m|mobile|cell|cellphone)[:\s]*([\d\-\.\s\(\)]{10,})', next_block.lower())
                    if mobile_search:
                        mobile = re.sub(r'[^\d]', '', mobile_search.group(1))  # Clean non-digit
                        mobile = f"{mobile[:3]}-{mobile[3:6]}-{mobile[6:]}"  # Format nicely

                    # Office number is other number
                    all_phones = re.findall(phone_pattern, next_block)
                    if all_phones:
                        for phone in all_phones:
                            # Clean and compare
                            clean_phone = re.sub(r'[^\d]', '', phone)
                            formatted_phone = f"{clean_phone[:3]}-{clean_phone[3:6]}-{clean_phone[6:]}"
                            if formatted_phone != mobile:
                                office = formatted_phone
                                break
                else:
                    # No mobile keywords, guess
                    if len(phones) >= 2:
                        office = phones[0]
                        mobile = phones[1]
                    elif len(phones) == 1:
                        office = phones[0]

            results.append({
                'Email': email,
                'Mobile': mobile,
                'Office': office
            })

            i += 2  # Skip next line also
        else:
            i += 1

    return results

# Streamlit app
st.title("Extract Emails, Mobile, and Office Numbers 📄📞")

uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type=["txt"])

st.write("OR")

text_input = st.text_area("Paste your text here:")

if st.button("Extract"):
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    elif text_input:
        text = text_input
    else:
        st.error("Please upload a file or paste some text.")
        st.stop()

    extracted_data = extract_contacts(text)
    df = pd.DataFrame(extracted_data)

    # Display results as a table
    st.subheader("Extracted Data Table")
    st.dataframe(df)

    # Format the extracted data for copy-pasting
    formatted_data = "\n".join(df.apply(lambda row: "\t".join(row.fillna('').astype(str)), axis=1))

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
