import base64
import mailparser

def parse_email():
    file = open('sample_data/email_data.txt')
    mail = mailparser.parse_from_string(file.read())
    print(mail.attachments)

if __name__ == "__main__":
    parse_email()