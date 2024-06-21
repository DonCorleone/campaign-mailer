import configparser
import csv
import datetime
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from postmarker.core import PostmarkClient
from postmarker.models.emails import EmailManager

# crate columnindexes for the csv file
columnIndexes = {
    'TemplateId': 0,
    'State': 99,
    'Year': 1,
    'Week': 2,
    'LastName': 3,
    'FirstName': 4,
    'Email': 5,
    'DateFrom': 6,
    'DateTo': 7,
    'Children': 99,
}

def extract_emails():
    # collect all the emails in a list
    emailsRaw = []

    # load the csv file in relative subfolder "mailing_lists"
    with open('mailing_lists/32402726_full.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            # skip the first line
            if reader.line_num == 1:

                # read cell by cell and check if the header is correct
                if row[columnIndexes['TemplateId']] != '_id':
                    print('Header not correct: TemplateId')
                    exit()
                if row[columnIndexes['Year']] != 'year':
                    print('Header not correct: year')
                    exit()
                if row[columnIndexes['Week']] != 'week':
                    print('Header not correct: week')
                    exit()
                if row[columnIndexes['LastName']] != 'lastName':
                    print('Header not correct: lastName')
                    exit()
                if row[columnIndexes['FirstName']] != 'firstName':
                    print('Header not correct: firstName')
                    exit()
                if row[columnIndexes['Email']] != 'email':
                    print('Header not correct: email')
                    exit()
                if row[columnIndexes['DateFrom']] != 'date_from':
                    print('Header not correct: date_from')
                    exit()
                if row[columnIndexes['DateTo']] != 'date_to':
                    print('Header not correct: date_to')
                    exit()
                # continue with the next line
                continue
                
            # skip empty lines
            if row[0] == '':
                continue
            # skip lines that do not have a valid mail address
            if '@' not in row[columnIndexes['Email']]:
                continue

            emailRaw = {
                'TemplateId': row[0],
                'From': 'anmeldungen@schlosswochen.ch',
                'To': row[columnIndexes['FirstName']] + ' ' + row[columnIndexes['LastName']] + ' <' + row[columnIndexes['Email']] + '>',
                'ToRaw': row[columnIndexes['Email']],
                'Week': row[columnIndexes['Week']],
                'Year': row[columnIndexes['Year']],
                'DateFrom': row[columnIndexes['DateFrom']],
                'DateTo': row[columnIndexes['DateTo']],
            }

            emailsRaw.append(emailRaw)

    # return the list of email dictionaries
    return emailsRaw

def create_image_attachment(filename):
    # Open the image file and read its contents
    with open(filename, "rb") as f:
        img_data = f.read()

    # Create image attachment object
    img = MIMEImage(img_data)

    img.add_header("Content-Disposition", "inline", filename=filename)
    # Set the content ID of the image attachment, without extension
    filenameWoExt = filename.split(".")[0]
    img.add_header("Content-ID", filenameWoExt)

    return img

def create_email_list(emailsRaw, attachments):
    emailList = list()
    for emailRaw in emailsRaw:
        # create the email-dictionary
        emailDict = {
            "From": emailRaw['From'],
            "To": emailRaw['To'],
            "TemplateId": emailRaw['TemplateId'],
            "TemplateModel": {
                "From": emailRaw['From'],
                "To": emailRaw['To'],
                "ToRaw": emailRaw['ToRaw'],
                "Year": emailRaw['Year'],
                "Week": emailRaw['Week'],
                "DateFrom": format_date(emailRaw['DateFrom']),
                "DateTo": format_date(emailRaw['DateTo']),
            },
            "Attachments": attachments
        }

        # add the emailDict to the list of dictionaries
        emailList.append(emailDict)
    return emailList

def format_date(date):
    # convert date from format 2023-07-10T07:00:00.000Z to 10.07.2023
    date = date.split("T")[0]
    date = datetime.strptime(date, "%Y-%m-%d")
    
    return date.strftime("%d.%m.%Y")

# collect all the emails in a list
emailsRaw = extract_emails()
img1 = create_image_attachment("image1.jpg")
emailList = create_email_list(emailsRaw, [img1])

# source the token out into a config file
config = configparser.ConfigParser()
# Read the configuration file
config.read('config.ini')

# Get the token value from the configuration file
token = config.get('Credentials', 'token')
postmark = PostmarkClient(server_token=token)

# ask the user if he wants to send the emails
print(f"Send {len(emailList)} emails? (y/n)")
answer = input()
if answer != 'y':
    print("Aborted")
    exit()

response = postmark.emails.send_template_batch(*emailList)
print(f"Response: {response}")
