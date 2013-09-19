#! /usr/bin/python
from smtplib import SMTP
from smtplib import SMTPException

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import COMMASPACE, formatdate

from data import db

import definitions
import decimal
D = decimal.Decimal

noreply = ''
fromNoReply = ''
ordersBox = ''


class Email():
    def __init__(self, sender, receiver, subject, plain, html):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.plain = plain
        self.html = html

    def send(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Smart Property Group <noreply@sptrust.co>'
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
            #need pass
            smtp.login('noreply@sptrust.co', 'noreply123noreply')
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
            smtp.quit()

            print 'Success: %s %s' % (self.sender, self.receiver)
        except SMTPException as e:
            print 'Fail: %s %s' % (self.sender, self.receiver)
            print e


def verificationPlain(url):
    plain = """
    Thank you for registering!\n
    You can now take the steps to become a Smart Property Group lender!\n
    Please visit the link below to confirm you are the owner of this email address.\n
    %s\n
    Smart Property Group 
    """ % url
    return plain


def verificationHtml(url):
    html = """
    <html>
    <p><b>Thank you for registering!</b></p>
    <p>You can now take the steps to become a Smart Property Group lender!</p>
    <p>Please visit the link below to confirm you are the owner of this email address.</p>
    <p>%s</p>
    <p><b>Smart Property Group</b></p>
    </html>
    """ % url
    return html


def transactionPendingMemoPlain(transaction):
    plain = """
    Congratulatuons! Your Smart Property Group transcation was successul!\n
    Transaction Id: %s\n
    Transaction Amount: %s\n
    Transaction Bitcoin Address: %s\n
    Smart Property Group 
    """ % (transaction.id, transaction.amount, transaction.bitcoinAddress)
    return plain


def transactionPendingMemoHtml(transaction):
    html = """
    <html>
    <p><b>Congratulations! Your Smart Property Group transaction was successful!</b></p>
    <p><b>Transaction Id:</b> %s</p>
    <p><b>Transaction Amount:</b> %s</p>
    <p><b>Transaction Bitcoin Address:</b> %s</p>
    <p><b>Smart Property Group</b></p>
    </html>
    """ % (transaction.id, transaction.amount, transaction.bitcoinAddress)
    return html


def transactionApprovalMemoPlain(transaction):
    plain = """
    Congratulatuons! Your Smart Property Group transaction was successul!\n
    Transaction Id: %s\n
    Transaction Amount: %s\n
    Transaction Bitcoin Address: %s\n
    Smart Property Group 
    """ % (transaction.id, transaction.amount, transaction.bitcoinAddress)
    return plain


def transactionApprovalMemoHtml(transaction):
    html = """
    <html>
    <p><b>Congratulations! Your Smart Property Group transaction was successful!</b></p>
    <p><b>Transaction Id:</b> %s</p>
    <p><b>Transaction Amount:</b> %s</p>
    <p><b>Transaction Bitcoin Address:</b> %s</p>
    <p><b>Smart Property Group</b></p>
    </html>
    """ % (transaction.id, transaction.amount, transaction.bitcoinAddress)
    return html


def transactionCancelationMemoPlain(transaction):
    plain = """
    Your Smart Property Group transaction was canceled!\n
    Transaction Id: %s\n
    Transaction Amount: %s\n
    Transaction Bitcoin Address: %s (invalid)\n
    Smart Property Group 
    """ % (transaction.id, transaction.amount, transaction.bitcoinAddress)
    return plain


def transactionCancelationMemoHtml(transaction):
    html = """
    <html>
    <p><b>Your Smart Property Group transaction was canceled!</b></p>
    <p><b>Transaction Id:</b> %s</p>
    <p><b>Transaction Amount:</b> %s</p>
    <p><b>Transaction Bitcoin Address:</b> %s (invalid)</p>
    <p><b>Smart Property Group</b></p>
    </html>
    """ % (transaction.id, transaction.amount, transaction.bitcoinAddress)
    return html
