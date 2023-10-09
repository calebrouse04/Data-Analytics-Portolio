# main.py
import re

def extract_info(filename):
    with open(filename, 'r') as file:
        content = file.read()
        
        # Regex for extracting phone numbers
        phone_pattern = re.compile(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})')
        
        # Regex for extracting email addresses
        email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})')
        
        phone_numbers = phone_pattern.findall(content)
        email_addresses = email_pattern.findall(content)
        
        return phone_numbers, email_addresses

def main():
    filename = 'text.txt'
    phone_numbers, email_addresses = extract_info(filename)
    
    print("Phone Numbers Found:")
    for number in phone_numbers:
        print(number)
    
    print("\nEmail Addresses Found:")
    for email in email_addresses:
        print(email)

if __name__ == "__main__":
    main()
