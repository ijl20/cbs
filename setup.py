# Run via:
# python manage.py shell
# >>> execfile('setup.py')

####################################################################################
##################### setup.py          ############################################
####################################################################################
#
# This file contains python statements that initialize the booking system database.
#
# *Before* this python script is run, the database should be emptied and
# re-initialized by running the ./reset script (which maps the Django models to the
# database).
#
# This python script is purely used to create the django objects (and hence the
# database data) for each of the rooms/crates in the system with the appropriate
# attributes.
#
# The data can most easily be editted by running the Django admin web interface, but
# the general idea is that in due course some decent 'edit' pages will be designed
# into the system.

#from django.utils.timezone import utc
import pytz

from datetime import datetime

from bookings.models import *

local_tz = pytz.timezone("Europe/London")

####################################################################################
print('Adding crate types (site, building, room)')
site = CrateType(name='Site')
site.save()

building = CrateType(name='Building', parent_crate_type=site)
building.save()

room = CrateType(name='Room', parent_crate_type=building)
room.save()

size = CrateAttributeType(id='size', crate_type=room, name="Seats", is_integer=True)
size.save()

####################################################################################
print('Adding permission types')

Permission( name='SuperUser',
            index=0,
            description='have administration rights over the whole system',
            ).save()
Permission( name='Admin',
            index=1,
            description='can perform all actions on the current resource',
            ).save()
Permission( name='Approver',
            index=2,
            description='can approve or cancel requests and existing bookings',
            ).save()
Permission( name='Booker',
            index=3,
            description='can directly book bookings without requiring approval',
            ).save()
Permission( name='Viewer',
            index=4,
            description='can view bookings and request new bookings requiring approval',
            ).save()
Permission( name='FreeBusyViewer',
            index=5,
            description='can view free/busy time and request new bookings requiring approval',
            ).save()

Permission( name='Self',
            index=6,
            description='can see own information and bookings',
            ).save()

####################################################################################
####################### Startup data for this system instance ######################
####################################################################################
print('Creating Crates')

nms = Crate(id="NMS",
    crate_type=site,
    short_name="New Museums Site",
    name="New Museums Site",
    map_url="http://map.cam.ac.uk/New+Museums+Site",
    description="Contains a mix of departments",
    location="Central Cambridge, between the Market and Pembroke Street")
    #note no calendar or parent_crate
    
nms.save()

austin = Crate(id="Austin",
    crate_type=building,
    parent_crate=nms,
    short_name="Austin Building",
    name="Austin Building",
    map_url="http://map.cam.ac.uk/Austin+Building",
    description="Where DNA was invented...",
    location="Through archway from Pembroke St")

austin.save()
    
au310 = Crate(id="Au310",
    crate_type=building,
    parent_crate=austin,
    short_name="Austin 310",
    name="Austin 310",
    map_url="http://map.cam.ac.uk/Austin+Building",
    description="Meeting room for 12",
    location="Access via main stairwell",
    calendar_id="cam.ac.uk_nbiik5kkvbok0n5mmfnhpihf1o@group.calendar.google.com",
    provisional_calendar_id="cam.ac.uk_pa7hgl4fi8v0hjsmo406mr3gdk@group.calendar.google.com",
    email="ijl20@cam.ac.uk",
    )
    
au310.save()

au311 = Crate(id="Au311",
    crate_type=building,
    parent_crate=austin,
    short_name="Austin 311",
    name="Austin 311",
    map_url="http://map.cam.ac.uk/Austin+Building",
    description="Ian Lewis office",
    location="3rd floor Austin Building, access via lift at either end of building",
    calendar_id="cam.ac.uk_o22gsn72482tdnta4ljl2dqd6g@group.calendar.google.com",
    email="ijl20@cam.ac.uk",
    image_list="2N43_1.jpg,thetford_1.jpg",
    )
    
au311.save()

cockcroft = Crate(id="Cockcroft",
    crate_type=building,
    parent_crate=nms,
    short_name="Cockcroft Building",
    name="Cockcroft Building",
    map_url="http://map.cam.ac.uk/Cockcroft+Building",
    description="With new Titan teaching rooms and Cockcroft Lecture Theatre",
    location="Through archway from Pembroke St",
    email="ijl20@cam.ac.uk",
    )

cockcroft.save()
    
new_titan1 = Crate(id="NewTitan1",
    crate_type=building,
    parent_crate=cockcroft,
    short_name="New Titan 1",
    name="New Titan Teaching Room 1",
    map_url="http://map.cam.ac.uk/Cockcroft+Building",
    description="40-seater computer-based teaching room maintained by the UCS",
    location="2nd floor Cockcroft Building, access via lift at corner with Austin Building",
    calendar_id="cam.ac.uk_vbqg92sa8a089eqe3l4bl4034g@group.calendar.google.com",
    email="ijl20@cam.ac.uk",
    )
    
new_titan1.save()

new_titan2 = Crate(id="NewTitan2",
    crate_type=building,
    parent_crate=cockcroft,
    short_name="New Titan 2",
    name="New Titan Teaching Room 2",
    map_url="http://map.cam.ac.uk/Cockcroft+Building",
    description="40-seater computer-based teaching room maintained by the UCS",
    location="2nd floor Cockcroft Building, access via lift at corner with Austin Building",
    calendar_id="cam.ac.uk_mtmsid6ohnvvlrh91n25c07tv0@group.calendar.google.com",
    provisional_calendar_id="cam.ac.uk_kgaj029113iorjcdde0pgb7sfk@group.calendar.google.com",
    email="ijl20@cam.ac.uk",
    )
    
new_titan2.save()

wcs = Crate(id="West",
    crate_type=site,
    short_name="West Cambridge Site",
    name="West Cambridge Site",
    map_url="http://map.cam.ac.uk/West+Cambridge+Site",
    description="Contains a mix of departments and other buildings",
    location="Accessed via Madingley Road")
    #note no calendar or parent_crate
    
wcs.save()

rnb = Crate(id="RNB",
    crate_type=building,
    #parent_crate=wcs,
    short_name="Roger Needham Building",
    name="Roger Needham Building",
    map_url="http://map.cam.ac.uk/Roger+Needham+Building",
    description="Home of Information Services (UCS + MISD)",
    location="On West Cambridge Site, behind the Computer Lab.",
    calendar_list="thetford,wisbech,huntingdon",
    email="reception@ucs.cam.ac.uk",
    image_list="rnb_1.png",
    )

rnb.save()
    
thetford = Crate(id="thetford",
    crate_type=room,
    parent_crate=rnb,
    short_name="Thetford",
    name="Thetford Room (12 seats)",
    map_url="http://map.cam.ac.uk/Roger+Needham+Building",
    description="12-seat meeting room",
    location="Ground floor of Roger Needham Building, adjacent to entrance lobby",
    calendar_id="cam.ac.uk_umufcojsv2iq0derm2jadfe434@group.calendar.google.com",
    calendar_web_color="#914D14",
    calendar_iframe_color="%236B3304", 
    provisional_calendar_id="cam.ac.uk_mjrfl24jdnfmr2fr6cj3i3bhbk@group.calendar.google.com",
    email="reception@ucs.cam.ac.uk",
    image_list="thetford_1.jpg",
    )
    
thetford.save()

wisbech = Crate(id="wisbech",
    crate_type=room,
    parent_crate=rnb,
    short_name="Wisbech",
    name="Wisbech Room (12 seats)",
    map_url="http://map.cam.ac.uk/Roger+Needham+Building",
    description="12-seat meeting room",
    location="2nd floor North Wing of Roger Needham Building, by Administration",
    calendar_id="cam.ac.uk_dvfqrdtig5giosh9o2bnqor2qo@group.calendar.google.com",
    calendar_web_color="#E0C240",
    calendar_iframe_color="%23AB8B00", 
    provisional_calendar_id="cam.ac.uk_r8ecpcfo1ifdq1f4sclcnjlu24@group.calendar.google.com",
    email="reception@ucs.cam.ac.uk",
    image_list="wisbech_1.jpg",
    )
    
wisbech.save()

huntingdon = Crate(id="huntingdon",
    crate_type=room,
    parent_crate=rnb,
    short_name="Huntingdon",
    name="Huntingdon Room (16+ seats)",
    map_url="http://map.cam.ac.uk/Roger+Needham+Building",
    description="16-seat meeting room",
    location="Ground floor South of Roger Needham Building, by entrance lobby",
    calendar_id="cam.ac.uk_mabnob73dn56aopnkjk1q2bhe8@group.calendar.google.com",
    calendar_web_color="#59BFB3",
    calendar_iframe_color="%231B887A", 
    provisional_calendar_id="cam.ac.uk_4ele24p4vqlv41v5fe6cijp3b0@group.calendar.google.com",
    email="reception@ucs.cam.ac.uk",
    image_list="huntingdon_1.jpg",
    )
    
huntingdon.save()

norwich = Crate(id="norwich",
    crate_type=room,
    parent_crate=rnb,
    short_name="Norwich",
    name="Norwich Auditorium (180 seats)",
    map_url="http://map.cam.ac.uk/Roger+Needham+Building",
    description="180-seat auditorium",
    location="Ground floor North of Roger Needham Building, by entrance lobby",
    calendar_id="cam.ac.uk_8all3l5hi5llaihlpg72lbacak@group.calendar.google.com",
    calendar_web_color="#536ca6",
    calendar_iframe_color="%23182C57", 
    provisional_calendar_id="cam.ac.uk_c17kvvsuc515me6f3gohbbrpag@group.calendar.google.com",
    email="reception@ucs.cam.ac.uk",
    image_list="norwich_1.jpg",
    )
    
norwich.save()


####################################################################################
print('Adding crate owners')

CrateOwner(crate=au310, instid='CS').save()
CrateOwner(crate=au311, instid='CS').save()
CrateOwner(crate=new_titan1, instid='CS').save()
CrateOwner(crate=new_titan2, instid='CS').save()

CrateOwner(crate=rnb, instid='CS').save()
CrateOwner(crate=thetford, instid='CS').save()
CrateOwner(crate=wisbech, instid='CS').save()
CrateOwner(crate=huntingdon, instid='CS').save()
CrateOwner(crate=norwich, instid='CS').save()

####################################################################################
print('Adding crate additional attributes')

CrateAttribute(crate=au310,attribute_type=size, attribute_int=12).save()
CrateAttribute(crate=au311,attribute_type=size, attribute_int=10).save()
CrateAttribute(crate=new_titan1,attribute_type=size, attribute_int=40).save()
CrateAttribute(crate=new_titan2,attribute_type=size, attribute_int=40).save()

CrateAttribute(crate=wisbech,attribute_type=size, attribute_int=12).save()
CrateAttribute(crate=thetford,attribute_type=size, attribute_int=12).save()
CrateAttribute(crate=huntingdon,attribute_type=size, attribute_int=40).save()
CrateAttribute(crate=norwich,attribute_type=size, attribute_int=180).save()

####################################################################################
print('Adding access permission rules for current crates')
    
Rule(crate = au310, permission = Permission.objects.get(name='Approver'), userid = 'ijl20',).save()
    
Rule(crate = au311, permission = Permission.objects.get(name='Admin'), userid = 'ijl20',).save()

Rule(crate = new_titan1, permission = Permission.objects.get(name='Booker'), groupid = '100850',).save()

Rule(crate = new_titan2, permission = Permission.objects.get(name='FreeBusyViewer'), instid = 'CS', ).save()

Rule(crate = austin, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'cbs.ALL',).save()
    
Rule(crate = cockcroft, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'cbs.ALL',).save()

Rule(crate = nms, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'cbs.ALL',).save()

Rule(crate = wcs, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'cbs.ALL',).save()

Rule(crate = rnb, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'cbs.ALL',).save()
Rule(crate = rnb, permission = Permission.objects.get(name='Viewer'), instid = 'CS',).save()
Rule(crate = rnb, permission = Permission.objects.get(name='Admin'), groupid='101603',).save()

####################################################################################
print('Adding some sample comments')

Comment(crate=au310, userid='ijl20', user_name='Ian Lewis', timestamp=local_tz.localize(datetime(2013,7,20,11,30)),
    text='First comment @ 11:30 for Au 310 from Ian').save()
Comment(crate=au310, userid='sk17', user_name='Steve Kearsey', timestamp=local_tz.localize(datetime(2013,7,20,14,30)),
    text='Second comment @ 14:30 for Au 310 from Steve').save()
Comment(crate=au311, userid='ijl20', user_name='Ian Lewis', timestamp=local_tz.localize(datetime(2013,7,20,11,30)),
    text='This is the HoD office so ccordinate with Lori Klimaszewska if you want to use it').save()
    
Comment(crate=thetford, userid='ijl20', user_name='Ian Lewis', timestamp=local_tz.localize(datetime(2013,8,20,11,30)),
    text='Immovable boardroom table with seating for 12.  Additional seating may be available around the perimeter of the room.  Capacity 12+.').save()
Comment(crate=wisbech, userid='ijl20', user_name='Ian Lewis', timestamp=local_tz.localize(datetime(2013,8,20,11,30)),
    text='Immovable boardroom table with seating for 12.  Additional seating may be available around the perimeter of the room.  Capacity 12+.').save()
Comment(crate=huntingdon, userid='ijl20', user_name='Ian Lewis', timestamp=local_tz.localize(datetime(2013,8,20,11,30)),
    text='Contains flexible folding tables and stackable chairs.  Suitable for a variety of layouts including theatre style and boardroom.  Capacity ~40 seated.').save()
    
Comment(crate=norwich, userid='ijl20', user_name='Ian Lewis', timestamp=local_tz.localize(datetime(2013,8,20,11,30)),
    text='The Norwich Auditorium in the Roger Needham Building seats 180 people and has full AV facilities').save()
    
####################################################################################
print('Adding some sample bookings')

Booking( 
    userid='ijl20',
    user_name='Ian Lewis',
    crate = au310,
    name = 'Test Au310 booking from Ian for Christmas Eve 2013',
    reference='1',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,24,11,30)),
    end = local_tz.localize(datetime(2013,12,24,12,30)),
    ).save()
    
Booking( 
    userid='sk17',
    user_name='Steve Kearsey',
    crate = au310,
    name = 'Au310 booking from Steve for Dec 25th 2013',
    reference='2',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    ).save()

Booking( 
    userid='ijl20',
    user_name='Ian Lewis',
    crate = au310,
    name = 'Requested Test Au310 booking from Ian for Christmas Eve 2013',
    reference='3',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,24,11,30)),
    end = local_tz.localize(datetime(2013,12,24,12,30)),
    pending = True,
    ).save()
    
Booking( 
    userid='sk17',
    user_name='Steve Kearsey',
    crate = au310,
    name = 'Requested Au310 booking from Steve for Dec 25th 2013',
    reference='4',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = True,
    ).save()

Booking( 
    userid='sk17',
    user_name='Steve Kearsey',
    crate = au311,
    name = 'Requested Au311 booking from Steve for Dec 25th 2013',
    reference='5',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = True,
    ).save()

Booking( 
    userid='sk17',
    user_name='Steve Kearsey',
    crate = new_titan1,
    name = 'Requested New Titan1 booking from Steve for Dec 25th 2013',
    reference='6',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = False,
    ).save()
    
Booking( 
    userid='ijl20',
    user_name='Ian Lewis',
    crate = new_titan1,
    name = 'Requested New Titan1 booking from Ian for Dec 25th 2013',
    reference='7',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = False,
    ).save()
    
Booking( 
    userid='sk17',
    user_name='Steve Kearsey',
    crate = new_titan1,
    name = 'Requested New Titan1 booking from Steve for Dec 25th 2013',
    reference='8',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = True,
    ).save()
    
Booking( 
    userid='ijl20',
    user_name='Ian Lewis',
    crate = new_titan1,
    name = 'Requested New Titan1 booking from Ian for Dec 25th 2013',
    reference='9',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = True,
    ).save()
    
Booking( 
    userid='sk17',
    user_name='Steve Kearsey',
    crate = new_titan2,
    name = 'New Titan2 booking from Steve for Dec 25th 2013',
    reference='10',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = False,
    ).save()
    
Booking( 
    userid='ijl20',
    user_name='Ian Lewis',
    crate = new_titan2,
    name = 'New Titan2 booking from Ian for Dec 25th 2013',
    reference='11',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = False,
    ).save()
    
Booking( 
    userid='sk17',
    user_name='Steve Kearsey',
    crate = new_titan2,
    name = 'Requested New Titan2 booking from Steve for Dec 25th 2013',
    reference='12',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = True,
    ).save()
    
Booking( 
    userid='ijl20',
    user_name='Ian Lewis',
    crate = new_titan2,
    name = 'Requested New Titan2 booking from Ian for Dec 25th 2013',
    reference='13',
    timestamp = local_tz.localize(datetime(2013,7,20,11,30)),
    start = local_tz.localize(datetime(2013,12,25,11,30)),
    end = local_tz.localize(datetime(2013,12,25,12,30)),
    pending = True,
    ).save()
    
####################################################################################
print('Creating Site definition for site "uis"')

Site(
    id='uis',
    instid = 'CS',
    app_name = 'RNB Booking System',
    home_title = '<h2>Welcome to the Information Services booking system</h2>',
    home_top = '<p>This system uses Google calendar to store the bookings</p>',
    # home_menu = models.TextField('Site title', max_length=4000, blank=True, null=True), # left menu of homepage
    home_bottom = '<p>Please call the Service Desk on 01223 (7)62999 if you have any queries about your bookings</p>',
    logo_url = 'http://www.cam.ac.uk',
    logo_image = 'images/logo.png',
    logo_alt = 'Cambridge University logo',
    # breadcrumbs = models.TextField('Site logo', max_length=1024, blank=True, null=True) # html initial breadcrumbs
    ).save()


    