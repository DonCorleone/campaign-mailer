import configparser
import csv
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from postmarker.core import PostmarkClient
from postmarker.models.emails import EmailManager

def extract_emails():
    # collect all the emails in a list
    emailsRaw = []

    # load the csv file in relative subfolder "mailing_lists"
    with open('mailing_lists/39387478.csv', newline='') as csvfile:
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
                if row[1] != 'title':
                    print('Header not correct: title')
                    exit()
                if row[2] != 'subject':
                    print('Header not correct: subject')
                    exit()
                if row[3] != 'year':
                    print('Header not correct: year')
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
                # continue with the next line
                continue
                
            # skip empty lines
            if row[0] == '':
                continue
            # skip lines that do not have a valid mail address
            if '@' not in row[6]:
                continue

            emailRaw = {
                'TemplateId': row[0],
                'MessageStream': 'broadcast',
                'From': 'no-replay@schlosswochen.ch',
                'To': row[4] + ' ' + row[5] + ' <' + row[6] + '>',
                'ToRaw': row[6],
                'Lastname' : row[4],
                'Surname' : row[5],
                'Title': row[1],
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

def create_email_list(emailsRaw):
    emailList = list()
    for emailRaw in emailsRaw:
        # create the email-dictionary
        emailDict = {
            "From": emailRaw['From'],
            "To": emailRaw['To'],
            "TemplateId": emailRaw['TemplateId'],
            "MessageStream": emailRaw['MessageStream'],
            "TemplateModel": {
                "From": emailRaw['From'],
                "To": emailRaw['To'],
                "ToRaw": emailRaw['ToRaw'],
                "Surname": emailRaw['Surname'],
                "Lastname": emailRaw['Lastname'],
            }
        }

        # add the emailDict to the list of dictionaries
        emailList.append(emailDict)
    return emailList

# collect all the emails in a list
emailsRaw = extract_emails()
emailList = create_email_list(emailsRaw)

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