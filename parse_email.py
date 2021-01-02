import base64
import email

def parse_email():
    file = open('sample_data/email_data.txt')
    message = email.message_from_string(file.read())
    all_payloads = message.get_payload()
    for payload in all_payloads:
        if payload.get_content_disposition() == "attachment" \
           and payload.get_content_type() == 'text/html':
            encoded_data = payload.as_string()
            data = base64.b64decode(encoded_data)
            html = data.decode('utf-8')
            print(html)

if __name__ == "__main__":
    parse_email()