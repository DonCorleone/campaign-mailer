import configparser
import csv
import datetime
from datetime import datetime
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

def extract_emails():
    # collect all the emails in a list
    emailsRaw = []

    # load the csv file in relative subfolder "mailing_lists"
    with open('mailing_lists/week-77.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            # skip the first line
            if reader.line_num == 1:
                continue
            # skip empty lines
            if row[0] == '':
                continue
            # skip lines that do not have the right length
            if len(row) != 9:
                continue
            # skip lines that do not have a valid mail address
            if '@' not in row[4]:
                continue
            # skip lines that do not have a valid name
            if row[5] == '':
                continue
            # skip lines that do not have a valid surname
            if row[6] == '':
                continue

            # create the email
            emailRaw = {
                'From': 'anmeldungen@schlosswochen.ch',
                'To': row[5] + ' ' + row[6] + ' <' + row[4] + '>',
                'ToRaw': row[4],
                'Lastname' : row[3],
                'Surname' : row[2],
                'Week': row[1],
                'Year': row[2],
                'DateFrom': row[7],
                'DateTo': row[8], 
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
            "TemplateId": 32327162,
            "TemplateModel": {
                "From": emailRaw['From'],
                "To": emailRaw['To'],
                "ToRaw": emailRaw['ToRaw'],
                "Surname": emailRaw['Surname'],
                "Lastname": emailRaw['Lastname'],
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

response = postmark.emails.send_template_batch(*emailList)
print(f"Response: {response}")
