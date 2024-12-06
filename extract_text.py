from bs4 import BeautifulSoup

# Load the HTML content
with open('mail_2024w.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract text content
text_content = soup.get_text(separator=' ', strip=True)

# Remove extra whitespace and blank lines
lines = [line.strip() for line in text_content.splitlines() if line.strip()]
cleaned_text_content = ' '.join(lines)

# Save the cleaned text content to a file
with open('mail_2024w.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_text_content)

print("Cleaned text content extracted and saved to mail_2024w.txt")