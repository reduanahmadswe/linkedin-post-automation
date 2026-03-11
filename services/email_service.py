import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import EMAIL_ADDRESS, EMAIL_PASSWORD

APPROVAL_URL = "http://localhost:8000/approve/"

def send_approval_email(post_id, content, topic):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = f"LinkedIn Post Approval: {topic}"

    body = f"Post Content:\n\n{content}\n\nApprove Link: {APPROVAL_URL}{post_id}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
