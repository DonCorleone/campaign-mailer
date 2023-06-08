import configparser
import csv
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from postmarker.core import PostmarkClient
from postmarker.models.emails import EmailManager
# open a csv file and send mails to the people in the file
# the csv file has to be in the same directory as this script
# the csv file has to be named "mails.csv"
# the csv file has to have the following structure:
#   - first line: header
#   - second line: mail addresses
#   - third line: names
#   - fourth line: surnames

# source the token out into a config file
config = configparser.ConfigParser()
# Read the configuration file
config.read('config.ini')

# Get the token value from the configuration file
token = config.get('Credentials', 'token')

# Open the image files and read their contents
with open("image1.jpg", "rb") as f:
    img1_data = f.read()

# Create image attachment objects
img1 = MIMEImage(img1_data)

# Set the content IDs of the image attachments
img1.add_header("Content-ID", "image1")

postmark = PostmarkClient(server_token=token)

# collect all the emails in a list
emailsRaw = []
    
# load the csv file
with open('mails.csv', newline='') as csvfile:
    # open a html file and read the html content
    with open('mail.html', 'r') as htmlfile:
        html = htmlfile.read()
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            # skip the first line
            if reader.line_num == 1:
                continue
            # skip empty lines
            if row[0] == '':
                continue
            # skip lines that do not have the right length
            if len(row) != 4:
                continue
            # skip lines that do not have a valid mail address
            if '@' not in row[1]:
                continue
            # skip lines that do not have a valid name
            if row[2] == '':
                continue
            # skip lines that do not have a valid surname
            if row[3] == '':
                continue

            # create the email
            emailRaw = {
                'From': 'linus@schlosswochen.ch',
                'To': row[2] + ' ' + row[3] + ' <' + row[1] + '>',
                'Surname' : row[2],
            }

            emailsRaw.append(emailRaw)

emailList = list()
for emailRaw in emailsRaw:
    # create the email-dictionary
    emailDict = {
        "From": emailRaw['From'],
        "To": emailRaw['To'],
        "TemplateId": 32013601,
        "TemplateModel": {
            "fizz": emailRaw['Surname']
        },
        "Attachments": [img1]
    }

    # add the emailDict to the list of dictionaries
    emailList.append(emailDict)

response = postmark.emails.send_template_batch(*emailList)
print(f"Response: {response}")
