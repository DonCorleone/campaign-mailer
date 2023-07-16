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
    with open('mailing_lists/recipients.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            # skip the first line
            if reader.line_num == 1:
                # header-row:
                # "_id","state","year","week","lastName","firstName","email","date_from","date_to","children[0].firstNameParticipant","children[0].lastNameParticipant","children[1].firstNameParticipant","children[1].lastNameParticipant"
                # if header is not correct: write to console which header not was correct and exit
                if row[0] != '_id':
                    print('Header not correct: _id')
                    exit()
                if row[1] != 'state':
                    print('Header not correct: state')
                    exit()
                if row[2] != 'year':
                    print('Header not correct: year')
                    exit()
                if row[3] != 'week':
                    print('Header not correct: week')
                    exit()
                if row[4] != 'lastName':
                    print('Header not correct: lastName')
                    exit()
                if row[5] != 'firstName':
                    print('Header not correct: firstName')
                    exit()
                if row[6] != 'email':
                    print('Header not correct: email')
                    exit()
                if row[7] != 'date_from':
                    print('Header not correct: date_from')
                    exit()
                if row[8] != 'date_to':
                    print('Header not correct: date_to')
                    exit()
                if row[9] != 'children[0].firstNameParticipant':
                    print('Header not correct: children[0].firstNameParticipant')
                    exit()
                if row[10] != 'children[0].lastNameParticipant':
                    print('Header not correct: children[0].lastNameParticipant')
                    exit()
                # continue with the next line
                continue
                
            # skip empty lines
            if row[0] == '':
                continue
            # skip lines that do not have a valid mail address
            if '@' not in row[6]:
                continue
            # skip lines that do not have a valid name
            if row[5] == '':
                continue
            # skip lines that do not have a valid surname
            if row[4] == '':
                continue

            # create the email
            # header-row:
            # "_id","state","year","week","lastName","firstName","email","date_from","date_to","children[0].firstNameParticipant","children[0].lastNameParticipant","children[1].firstNameParticipant","children[1].lastNameParticipant"
 
            # initialize an array of string
            children = []
            children.append(
                row[9] + ' ' + row[10]
            )

            # append row [11] if not empty to children
            if row[11] != '':
                children.append(
                    row[11] + ' ' + row[12]
                )
            
            # append row [13] if existing AND if not empty to children
            if len(row) > 13:
                if row[13] != '':
                    children.append(
                        row[13] + ' ' + row[14]
                    )

            # append row [15] if existing AND if not empty to children
            if len(row) > 15:
                if row[15] != '':
                    children.append(
                        row[15] + ' ' + row[16]
                    )      

            # create string of children, comma separated, childrens containment
            children = ', '.join(children)

            emailRaw = {
                'TemplateId': row[0],
                'From': 'anmeldungen@schlosswochen.ch',
                'To': row[5] + ' ' + row[4] + ' <' + row[6] + '>',
                'ToRaw': row[6],
                'Lastname' : row[4],
                'Surname' : row[5],
                'Week': row[3],
                'Year': row[2],
                'DateFrom': row[7],
                'DateTo': row[8],
                'Children': children
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
                "Surname": emailRaw['Surname'],
                "Lastname": emailRaw['Lastname'],
                "Year": emailRaw['Year'],
                "Week": emailRaw['Week'],
                "DateFrom": format_date(emailRaw['DateFrom']),
                "DateTo": format_date(emailRaw['DateTo']),
                "Children": emailRaw['Children'],
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
