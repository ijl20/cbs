# Cambridge Booking System

This demonstrator system was built (by me) in 2013 as a practical illustration of what a room-booking system 
fit-for-purpose for the Collegiate University. As a "room booking" system it has capabilities the UIS is unlikely 
to achieve but they're worth capturing:

(1) GENERALIZATION OF BOOKABLE ASSETS: The bookable assets are in a general hierarchy and there is nothing special about a 
room / building / site, i.e. the system is equally usable for equipment. Bookings are possible at all 
levels of the hierarchy which works for dividable rooms but also e.g. for AV equipment which is dividable. 
This flexible structure is supported by an equally flexible permissions structure, see (2,3).

(2) AUTHORIZATION USING LOOKUP: The system uses UIS Lookup for its permission model, i.e. assets can be protected
at the level of individuals (i.e. crsids), Lookup institutions (e.g. CL, UIS) and Lookup groups. The 
permission rules for assets are simple and declarative. A simple rule set for a CL meeting room would be 
a 'group' as the administrators, another 'group' to approve repeat bookings, members of inst 'CL' can book 
the room and see the events, all people can see free-busy and request a booking. If not set on an 
individual asset, rules are inherited from parent assets - typically this means rules do not need to be set
on individual meeting rooms but can inherit the rules for the building.

(3) FEDERATED DESIGN: The fundamental design of the system is to provide a single platform that appears 
federated and permissive. I.e. the person that adds an asset to the system has the opportunity to decide 
the access rules so a department can manage assets that are not visible outside of a single research group,
or lecture theatres can be visible across the university. The system is designed for thousands of assets, 
many of which may be individually, team or department owned, not just a few centrally managed lecture theatres. 
This means a department or College can add assets to the system without them being visible outside their 
institution which might sound problematic to a central administration but is healthy for the adoption of 
the platform.

(4) CALENDARING: Google Calendar is used to display the room bookings, embedded into the web application 
for full functionality but also can be viewed independently or directly accessed via any other route. 
The application uses the Google Calendar API such that the Google platform provides cloud storage for 
the asset bookings and much of the Google Calendar functionality benefits users viewing the room calendars. 
For effective support, each asset has two Google calendars - one for confirmed bookings and another for 
requested bookings - these are typically displayed overlayed in different colours and are easy to interpret.

(5) ATTRIBUTE LIST: A few asset attributes are standardised (like identifier, name, description, image, 
location) but the list of attributes is generalised, so a room may have a seating capacity and projector 
while equipment might have a wattage. I would expect these attributes (and the calendar bookings) provide 
a good basis for a search capability which was not implemented in the prototype.

## Common misunderstandings

There are a few misunderstandings I learned during the brief period of this demonstrator development
and its subsequent use in the UIS which are certain to be repeated and worth recording:

(6) Estates colleagues focus almost entirely on the linear list of attributes that can be associated 
with a room, rather than the features of the platform that make it usable from a department, college or 
individual perspective. I.e. they were impressed that the demonstrator can include one or more images 
of the room, and a reference presented on a map, and asked if additional attributes could be added like 
he cleaning schedule and what was in the room.

(7) Colleagues with administrative responsibility typically have a strong belief that everything to do 
with bookable assets should have a human approval in the loop. The permissive approach in my demonstrator 
allows ALL levels of permission from completely central administration through to individual management of 
assets and in every case an administrator would suggest the appropriate configuration of every asset was 
with the administrator able to make changes and the end-user to only request things. There is a lack of interest 
or understanding of difference between, say, lecture theatres and an ante-room to my office. I am confident 
users should be able to add assets to the system without administrative intervention - a department, faculty, 
school or university can decide the appropriate 'ownership' of a meeting room or lecture theatre and not 
constrain the entire system with a manual administrative process of adding assets.

(8) 'Search' is given undue precedence in booking systems. It's a useful feature but very secondary to 
browsing a calendar showing the bookings of an asset you might already know you are interested in. I would 
express caution when hearing arguments that it might be a valuable use-case that people search an entire 
campus or city for a room rather than within the building in which they work - there is little evidence this 
would be common practice even if available.

(9) As an adjunct to (8), the 'calendar view' of asset bookings is underestimated with system developers 
commonly believing an in-application calendar is going to be adequate for end-user access and departmental 
integration. It has become very unlikely that the limited resources applied to calendars developed *within* 
room booking software can compete with the cloud solutions provided by Google and Microsoft and the in-system 
approach for calendars is naive.

(10) In the 'permissions model', adding an asset to the system is often assumed to require explicitly assigned 
permission from a central administrator to the individual concerned. As long as assets cannot be added 
anonymously this is a flawed assumption.

# Install notes

## APACHE2:

1) Install mod_wsgi

2) Set up suitable vhost
2.1) Copy required directives into vhosts/<hostmame>.conf file
2.2) Adjust directory names as appropriate

## PYTHON:

1) Install python 2.X

2) Additional modules:
* python-django
* google-api-python-client
* python-pyOpenSSL
* python-pycrypto
* python-pytz
* python-httplib2
* python-python-gflags


## CBS:

1) copy cbs directory

2) If using SQLITE3:
2.1) Create sqlite3 directory with a+w permission
2.2) Create sqlite3/cbs directory with a+w permission
2.3) NOTE step 5.2 below

3) Modify hard-coded directory references
3.1) Edit cbs/cbs/settings.py and check directory references match your system
3.2) Edit cbs/cbs/wsgi.py and check directory references match your system
3.3) Edit cbs/bookings/cam_email.py and update system_url
3.4) Edit cbs/bookings/cam_cal.py and update KEY_FILE
4) cd into cbs directory
4.1) Ensure log/django/cbs.log has a+w permission

5) Set up database
5.1) run "./reset" to initialize sqlite3 database
5.2) chmod the sqlite3/cbs file to a+w (i.e. this is the CBS database)

6) run "python manage.py shell"
6.1) >>>execfile('setup.py') to populate database with initial data e.g. room definitions

7) If only running a python dev webserver: run "python manage.py runserver 0.0.0.0:8080"

7.1) point browser to <hostname>:8080

## TO RESTART WEB SERVER:

sudo /usr/sbin/crm resource restart res_www_server

## TO RUN PYTHON COMMANDS AGAINST DATABASE:

python manage.py shell
