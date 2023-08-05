import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
mail_to = 'rli@veritionfund.com'
html_head = '''
<html>
    <head>
        <script>
            function displayResult(){
                    document.getElementById('p1').style.font-family='Consolas';
                    document.getElementById('p1').style.fontSize='medium';
            }
        </script>
    </head>
<pre><p1>
'''

html_tail = '''</p1></pre></html>'''

    
def send(from_address='infra@veritionfund.com', to_address=mail_to, subject="htmlmail", body=""):
    msg = MIMEMultipart('alternative')
    msg['Subject']  = subject
    msg['From']     = from_address
    msg['To']       = to_address
    
    html = MIMEText(html_head+body+html_tail, 'html')
    msg.attach(html)
    s = smtplib.SMTP('localhost')
    s.sendmail(from_address, msg['To'].split(","), msg.as_string())

if __name__ == '__main__':
    from_address = 'infra@veritionfund.com'
    to_address = 'rli@veritionfund.com'
    subject = 'test'
    body = 'test'
    send(from_address, to_address, subject, body)
    