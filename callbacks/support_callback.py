from dash import Output, Input, State
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import smtplib

# Load environment variables from .env file
load_dotenv()

def support_callback(app):
        
    @app.callback(
        Output('support-status', 'children'),
        Input('support-send-button', 'n_clicks'),
        State('name-input', 'value'),
        State('email-input', 'value'),
        State('message-input', 'value')
    )

    def send_email(n_clicks, name, email, message):
        if n_clicks > 0:
            if not (name and email and message):
                return 'Please fill out all fields'

            myEmail = os.getenv('EMAIL')
            myPassword = os.getenv('EMAIL_PASSWORD')
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            supportEmail_Shyam = 'shyam.desai@mail.mcgill.ca'
            supportEmail_Masa = 'email@masakagami.com'

            # Email to support team
            support_msg = MIMEMultipart()
            support_msg['From'] = myEmail
            support_msg['To'] = supportEmail_Masa
            support_msg['Subject'] = f"Support Request from: {name}"

            support_body = f"""
            Support Request Details:
            ------------------------
            Name: {name}
            Email: {email}

            Message:
            {message}
            """
            support_msg.attach(MIMEText(support_body, 'plain'))

            # Email to user
            user_msg = MIMEMultipart()
            user_msg['From'] = myEmail
            user_msg['To'] = email
            user_msg['Subject'] = "Thank you for contacting Budgetr Support"

            user_body = f"""
            Dear {name},

            Thank you for reaching out to Budgetr support. We have received your message and will get back to you as soon as possible.

            Here is a copy of your message:
            -------------------------------

            {message}

            Best regards,
            The Budgetr Support Team
            """
            user_msg.attach(MIMEText(user_body, 'plain'))
            
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(myEmail, myPassword)

                # Send support email to the creators and thank you email to the user
                server.sendmail(myEmail, supportEmail_Shyam, support_msg.as_string())
                server.sendmail(myEmail, supportEmail_Masa, support_msg.as_string())
                server.sendmail(myEmail, email, user_msg.as_string())

                server.quit()
                return 'Email sent successfully'
            except Exception as e:
                return 'Error sending email: {}'.format(e)
        return ''