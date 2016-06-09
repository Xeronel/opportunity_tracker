from datetime import datetime
from email.mime.text import MIMEText
import smtplib
import psycopg2
import config


def send_notifications():
    # Open a connection to the database
    conn = psycopg2.connect(database=config.db.database,
                            user=config.db.username,
                            password=config.db.password,
                            host=config.db.hostname,
                            port=config.db.port)
    conn.set_session(autocommit=True)
    cursor = conn.cursor()

    # Get a list of notifications that need to be sent
    cursor.execute("WITH updt (employee, company, note) AS ("
                   "UPDATE notification SET sent = TRUE "
                   "WHERE notify_date = %s AND sent = FALSE "
                   "RETURNING employee, company, note) "
                   "SELECT employee.email, company.name, updt.note "
                   "FROM updt, employee, company "
                   "WHERE employee.id = updt.employee AND company.id = updt.company;",
                   [datetime.today().strftime('%Y-%m-%d')])
    notifications = cursor.fetchall()

    # Group emails by employee and company
    emails = {}
    for employee, company, note in notifications:
        if employee not in emails:
            emails[employee] = {}
        if company not in emails[employee]:
            emails[employee][company] = '%s' % note
        else:
            emails[employee][company] += "<br>%s" % note

    # Connect to SMTP Server
    try:
        conn = smtplib.SMTP(host=config.smtp.hostname, port=config.smtp.port)
        conn.set_debuglevel(False)
        if config.smtp.username or config.smtp.password:
            conn.login(config.smtp.username, config.smtp.password)
    except Exception as e:
        print("mail failed; %s" % str(e))
        conn.quit()
        return

    # Send an email to each employee
    for employee, companies in emails.items():
        html = '<html><head></head><body>'

        # Build Email
        for company, note in companies.items():
            html += '<h2>%s</h2>\r%s' % (company, note)
        email = MIMEText(html, 'html')
        email['From'] = config.smtp.sender
        email['Subject'] = 'Opportunity Tracker Notifications'
        email['To'] = employee
        try:
            conn.send_message(email)
        except Exception as e:
            print("Mail failed to send. %s" % str(e))
    conn.quit()


if __name__ == '__main__':
    send_notifications()
