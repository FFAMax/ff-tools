import smtplib
from email.mime.text import MIMEText
from email.header import Header

# SMTP server settings
smtp_server = "example.com"
smtp_port = 25
smtp_user = "sender@example.com"
smtp_password = "edbflccuihrivevgbivtnttbctbilcfu"

# Email content
from_email = "sender@example.com"
to_email = "ffamax@gmail.com"
subject = "Test Email"
body = "This is a test email"

# Create a MIMEText object
msg = MIMEText(body, "plain", "utf-8")
msg["From"] = Header(from_email, "utf-8")
msg["To"] = Header(to_email, "utf-8")
msg["Subject"] = Header(subject, "utf-8")

# Send email using SMTP over TLS
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)  # Show debug messages and log the conversation
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()
    print("Email sent successfully!")
except smtplib.SMTPException as e:
    print("Error sending email:", e)

