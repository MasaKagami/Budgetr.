from dash import Output, Input, State
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def support_callback(app):
        
    @app.callback(
        Output('output-state', 'children'),
        Input('send-button', 'n_clicks'),
        State('name-input', 'value'),
        State('email-input', 'value'),
        State('message-input', 'value')
    )

    def send_email(n_clicks, name, email, message):
        if n_clicks > 0:
            myEmail = 'email@masakagami.com'
            myPassword = 'masaand$teph100'
            smtp_server = 'smtp.office365.com'
            smtp_port = 587

            msg = MIMEMultipart()
            msg['From'] = myEmail
            msg['To'] = email
            msg['Subject'] = "Support Request from: " + name

            body = "Name: {}\nEmail: {}\nMessage: {}".format(name, email, message)
            msg.attach(MIMEText(body, 'plain'))
            
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(myEmail, myPassword)
                text = msg.as_string()
                server.sendmail(myEmail, email, text)
                server.quit()
                return 'Email sent successfully'
            except Exception as e:
                return 'Error sending email: {}'.format(e)
        return ''