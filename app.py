import pandas as pd
import re

def extract_contacts(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    mobile_keywords = ['cell', 'c:', 'mobile', 'm:']
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    results = []
    current = {}

    for line in lines:
        # Extract emails
        email_match = re.search(email_pattern, line)
        if email_match:
            if current:
                results.append(current)
                current = {}
            current['Email'] = email_match.group(0)

        # Extract phones
        phones = re.findall(phone_pattern, line)
        if phones:
            lower_line = line.lower()
            if '|' in line:
                # If phones separated by |
                if len(phones) >= 2:
                    current['Office'] = phones[0]
                    current['Mobile'] = phones[1]
            elif any(keyword in lower_line for keyword in mobile_keywords):
                # If mobile keyword present
                current['Mobile'] = phones[0]
            else:
                # Otherwise treat as Office number
                if 'Office' not in current:
                    current['Office'] = phones[0]
                else:
                    current['Mobile'] = phones[0]

    # Save last record
    if current:
        results.append(current)

    return results

# Example usage:
text = """(paste your text here)"""
data = extract_contacts(text)
df = pd.DataFrame(data)
print(df)
