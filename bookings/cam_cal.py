
import httplib2

from apiclient.discovery import build

from pprint import pprint
import sys

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from cbs_settings import CBS_Settings

from .models import Booking, Crate

# timezone stuff
from datetime import datetime, timedelta

from .cam_connect import CamConnect

import pytz

KEY_FILE = CBS_Settings.FILE_BASE+'/434d2860388d9dc3b937ad604500bb33a056ac3f-privatekey.p12'
SERVICE_ACCOUNT = '840251059696@developer.gserviceaccount.com'
LOCAL_TIMEZONE = 'Europe/London'

class CamCal:
    
    def __init__(self, request):
        self.request = request
        #self.form_data = data_from_form
        # Load the key in PKCS 12 format that you downloaded from the Google API
        # Console when you created your Service account.
        f = file(KEY_FILE, 'rb')
        key = f.read()
        f.close()

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with the Credentials. Note that the first parameter, service_account_name,
        # is the Email address created for the Service account. It must be the email
        # address associated with the key that was created.
        credentials = SignedJwtAssertionCredentials(
          SERVICE_ACCOUNT,
          key,
          scope='https://www.googleapis.com/auth/calendar')
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Build a service object for interacting with the API.
        self.service = build("calendar", "v3", http=http)

        
    def book(self, booking):
        ###################################################################
        # add event
        
        start_utc = booking.start
        end_utc = booking.end
        
        
        year = str(start_utc.year)
        month = ("0"+str(start_utc.month))[-2:]
        day = ("0"+str(start_utc.day))[-2:]
        hour = ("0"+str(start_utc.hour))[-2:]
        min = ("0"+str(start_utc.minute))[-2:]
        
        # here we build the START string for Google
        start_str = year+"-"+month+"-"+day+"T"+hour+":"+min+":00.0z"
        
        year = str(end_utc.year)
        month = ("0"+str(end_utc.month))[-2:]
        day = ("0"+str(end_utc.day))[-2:]
        hour = ("0"+str(end_utc.hour))[-2:]
        min = ("0"+str(end_utc.minute))[-2:]
        
        # here we build the END string for Google
        end_str = year+"-"+month+"-"+day+"T"+hour+":"+min+":00.0z"
        
        event_details = {
        #  "attendees": [ {"email":"ijl20@cam.ac.uk"} ],
          "start": { "dateTime": start_str },
          "end":   { "dateTime": end_str },
          "summary": booking.name,
          "location": booking.crate.name,
          #"colorId": "3"
        }
        
        calendar_id = booking.crate.calendar_id
        if booking.pending and booking.crate.provisional_calendar_id:
            calendar_id = booking.crate.provisional_calendar_id
            
        # PUT ENTRY FOR BOOKING IN GOOGLE CALENDAR
        event = self.service.events().insert(calendarId=calendar_id, body=event_details).execute()
        
        #r_string = "start:"+str(start)+"/start_str"+start_str + "/" + end_str + "/" + form_data['crate_id']
        #r_string += "/"+Booking.objects.all()[0]
        return event
        
    def cancel(self, booking):
        # choose which calendar contains this booking
        calendar_id = booking.crate.calendar_id
        if booking.pending and booking.crate.provisional_calendar_id:
            calendar_id = booking.crate.provisional_calendar_id
        # remove booking from appropriate calendar
        try:
            self.service.events().delete(calendarId=calendar_id, eventId=booking.reference).execute()
        except:
            # do nothing
            pass
        # remove booking from database
        booking.delete()
        return True

