#! /usr/bin/python
from smtplib import SMTP
from smtplib import SMTPException

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import COMMASPACE, formatdate

from data import db

import definitions

noreply = 'noreply@hypewhiz.com'

class Email():
    def __init__(self, sender, receiver, subject, plain, html):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.plain = plain
        self.html = html

    def send(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Hype Wizard <noreply@hypewhiz.com>'
        msg['To'] = self.receiver
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        part1 = MIMEText(self.plain, 'plain')
        part2 = MIMEText(self.html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        try:
            smtp = SMTP('smtp.mailgun.org', 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login('noreply@hypewhiz.com', 'noreply123noreply')
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
            smtp.quit()

            print 'Success: %s => %s' % (self.sender, self.receiver)
        except SMTPException as e:
            print 'Fail: %s => %s' %  (self.sender, self.receiver)
            print e


def verificationPlain(url):
    plain = """
    Thank you for registering!\n
    You can now take the steps to become a Hype Wizard user!\n
    Please visit the link below to confirm you are the owner of this email address.\n
    %s\n
    Hype Wizard Team
    """ % url
    return plain


def verificationHtml(url):
    html = """
    <html>
    <p><b>Thank you for registering!</b></p>
    <p>You can now take the steps to become a Hype Wizard user!</p>
    <p>Please visit the link below to confirm you are the owner of this email address.</p>
    <p>%s</p>
    <p><b>Hype Wizard Team</b></p>
    </html>
    """ % url
    return html


def verify_email_memo_plain(url):
    plain = """
    Please visit the link below to confirm you are the owner of this email address.\n
    %s\n
    Hype Wizard Team
    """ % url
    return plain


def verify_email_memo_html(url):
    html = """
    <html>
    <p>Please visit the link below to confirm you are the owner of this email address.</p>
    <p>%s</p>
    <p><b>Hype Wizard Team</b></p>
    </html>
    """ % url
    return html


def offer_created_memo_plain(promoter, offer):
    plain = """
    You have received an offer to promote one of your tweets.\n
    Promoter Twitter Name: %s\n
    Tweet Id: %s\n
    Please login to review promoter's wizard score before you continue.\n
    Hype Wizard Team
    """ % (promoter.twitter_name, offer.twitter_status_id)
    return plain


def offer_created_memo_html(promoter, offer):
    html = """
    <html>
    <p>You have received an offer to promote one of your tweets.</p>
    <p><b>Promoter: </b><a:href="http://www.twitter.com/%s">%s</a></p>
    <p><b>Tweet Id: </b>%s</p>
    <p>Please login to review promoter's wizard score before you continue.</p>
    <p><b>Hype Wizard Team</b></p>
    </html>
    """ % (promoter.twitter_name, promoter.twitter_name, offer.twitter_status_id)
    return html


def offer_approved_memo_plain(offer):
    plain = """
    Your Hype Wizard offer has been approved.\n
    Please retweet status #%s for your client before you can claim reserved funds.\n
    Hype Wizard Team
    """ % offer.twitter_status_id 
    return plain


def offer_approved_memo_html(offer):
    html = """
    <html>
    <p>Your Hype Wizard offer has been approved.</p>
    <p>Please retweet status #%s for your client before you can claim reserved funds.</p>
    <p><b>Hype Wizard Team</b></p>
    </html>
    """ % offer.twitter_status_id 
    return html


def password_reset_memo_plain(email, password):
    plain = """
    Account Details\n
    Email: %s\n
    Temporary Password: %s\n
    Hype Wizard Team
    """ % (email, password)
    return plain


def password_reset_memo_html(email, password):
    html = """
    <html>
    <p><h2>Account Details</h2></p>
    <p><b>Email:</b> %s</p>
    <p><b>Temporary Password:</b> %s</p>
    <p><b>Hype Wizard</b></p>
    </html>
    """ % (email, password)
    return html


def promotion_request_memo_plain():
    plain = """
    You have a pending request for promotion at Hype Wizard.\n
    Hype Wizard Team
    """ 
    return plain


def promotion_request_memo_html():
    html = """
    <html>
    <p>Your have a pending request for promotion at Hype Wizard.</p>
    <p><b>Hype Wizard Team</b></p>
    </html>
    """
    return html
