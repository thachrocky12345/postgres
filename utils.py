import smtplib
import email.mime.multipart as Mulitpart
import email.mime.text as MimeText



def send_email_notice(message_input, email_recipients="tbui@farmobile.com"):
    '''
    Send email notice installation is done
    '''

    subject_message = "Linux Installation Report"
    server = smtplib.SMTP('smtp.gmail.com:587')
    username = "kcmicrobiome@gmail.com"
    passw = "123456Thach"
    server.ehlo()
    server.starttls()
    server.login(username, passw)
    for address in email_recipients.split(","):
        address = address.strip()
        message = "From: %s \n Subject: %s \n\n" % (username,subject_message)
        message += "\n %s\n" % message_input
        server.sendmail(username, address, message)
    server.quit()


def send_email_notice_new(subject, msg_error, recipients='thachrocky@icloud.com'):

    sender = "thach.bui@gmail.com"
    recipient = [i.strip() for i in recipients.split(',')]

    msg = Mulitpart.MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipient)

    msg.attach(MimeText.MIMEText(msg_error, 'html'))

    # send it
    email = smtplib.SMTP('localhost', 25)
    try:
        email.sendmail(sender, recipient, msg.as_string())
    finally:
        email.quit()

if __name__ == '__main__':
    # send_email_notice("test", "not_error")
    send_email_notice("test")