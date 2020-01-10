import smtplib

from email.MIMEText import MIMEText
from email.Utils import formatdate

import pytz
from datetime import datetime

from cbs_settings import CBS_Settings
CRLF = "\r\n"

class CamEmail:
    
    def __init__(self):
        self.system_email = CBS_Settings.SYSTEM_EMAIL
        self.system_url = CBS_Settings.SYSTEM_URL
        self.local_tz = pytz.timezone(CBS_Settings.SYSTEM_TIMEZONE)

    def send_request(self, booking):
        booking_timestamp = booking.start.astimezone(self.local_tz)

        body = self.system_url + booking.crate.id + "/" + CRLF + CRLF
        body += "Booking request from " + booking.user_name + CRLF
        body += "for " + booking.crate.name + " on " + booking_timestamp.strftime("%d %b %Y") + CRLF + CRLF
        
        body += "Description: "+booking.name + CRLF
        
        msg = MIMEText(body,'plain')
        msg['Subject'] = "Booking request for "+booking.crate.id
        msg['To'] = booking.crate.email
        self.send_mail(msg)
        
    def send_mail(self, msg):
        msg['Reply-To']=self.system_email
        msg['Date'] = formatdate(localtime=True)
        msg['From'] = self.system_email

        mailServer = smtplib.SMTP('ppsw.cam.ac.uk', 25)
        #mailServer = smtplib.SMTP('smtp.hermes.cam.ac.uk', 587)
        #mailServer.ehlo()
        #mailServer.starttls()
        #mailServer.ehlo()
        #mailServer.login(self.login, self.password)
        mailServer.sendmail(self.system_email, [msg['To']], msg.as_string())
        mailServer.close()
    
    def send_cancellation(self, booking):
        if not booking.user_email:
            return
        booking_timestamp = booking.start.astimezone(self.local_tz)
        body = self.system_url + booking.crate.id + "/" + CRLF + CRLF
        body += "THE FOLLOWING BOOKING REQUEST CANNOT BE FULFILLED:" + CRLF + CRLF
        body += "Booking request from " + booking.user_name + CRLF
        body += "for " + booking.crate.name + " on " + booking_timestamp.strftime("%d %b %Y") + CRLF + CRLF
        
        body += "Description: "+booking.name + CRLF
        
        msg = MIMEText(body,'plain')
        msg['Subject'] = "Booking request cancelled for "+booking.crate.id
        msg['To'] = booking.user_email
        self.send_mail(msg)
    
    def send_approval(self, booking):
        if not booking.user_email:
            return
        booking_timestamp = booking.start.astimezone(self.local_tz)
        body = self.system_url + booking.crate.id + "/" + CRLF + CRLF
        body += "THE FOLLOWING BOOKING REQUEST HAS BEEN APPROVED:" + CRLF + CRLF
        body += "Booking request from " + booking.user_name + CRLF
        body += "for " + booking.crate.name + " on " + booking_timestamp.strftime("%d %b %Y") + CRLF + CRLF
        
        body += "Description: "+booking.name + CRLF
        
        msg = MIMEText(body,'plain')
        msg['Subject'] = "Booking request approved for "+booking.crate.id
        msg['To'] = booking.user_email
        self.send_mail(msg)
    
    