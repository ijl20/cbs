####################################################################################
print('Adding NMS UIS rooms')

from bookings.models import *

room = CrateType.objects.get(name="Room")

cockcroft = Crate.objects.get(id="Cockcroft")

size = CrateAttributeType.objects.get(id="size")

## C402 UIS Meeting Room
c402 = Crate(id="c402",
    crate_type=room,
    parent_crate=cockcroft,
    short_name="C402 UIS Mtg Rm",
    name="Cockcroft 4 Chatteris UIS Meeting Room",
    map_url="http://map.cam.ac.uk/Cockcroft+Building",
    description="A UIS meeting room, takes up to 18 people comfortably. This room will be equipped with projector, flat screen, telephone, ability to videoconference (both hardware codec and webconference solutions). It can be booked for any type of meeting including union meetings.",
    location="4th floor Cockcroft Building, access via lift at corner with Austin Building",
    calendar_web_color="#914D14",
    calendar_iframe_color="%236B3304", 
    calendar_id="cam.ac.uk_j30rsg4atit0jepuqiu53jagvs@group.calendar.google.com",
    provisional_calendar_id="cam.ac.uk_84ke820r406h1h9vhmeje1lee4@group.calendar.google.com",
    email="reception@ucs.cam.ac.uk",
    )
    
c402.save()

CrateOwner(crate=c402, instid='UIS').save()

CrateAttribute(crate=c402,attribute_type=size, attribute_int=18).save()

Rule(crate = c402, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'cbs.ALL', ).save()
Rule(crate = c402, permission = Permission.objects.get(name='Viewer'), instid = 'CS',).save()
Rule(crate = c402, permission = Permission.objects.get(name='Admin'), groupid='101603',).save()

## C4 UIS Breakout space
c4breakout = Crate(id="c4breakout",
    crate_type=room,
    parent_crate=cockcroft,
    short_name="C4 UIS Breakout",
    name="Cockcroft 4 UIS Breakout Space",
    map_url="http://map.cam.ac.uk/Cockcroft+Building",
    description="Jointly with Archaeology, the area also provides our two departments with a huge open area, parquet-floored.   Photography and Illustration Service (PandIS) are going to install some of their exhibition photos along the vast magnolia-coloured wall.  We have some spare tables and chairs which will be put into the area.  This area will be available as both a breakout space from courses (eg courses in the Titan rooms), and may be used as a PandIS exhibition space for future exhibitions too.  It is also available to any of us requiring a large breakout or gathering space in the city centre for work purposes.",
    location="4th floor Cockcroft Building, access via lift at corner with Austin Building",
    calendar_web_color="#E0C240",
    calendar_iframe_color="%23AB8B00", 
    calendar_id="cam.ac.uk_ug4i0n610najjl98diah76nt8c@group.calendar.google.com",
    provisional_calendar_id="cam.ac.uk_1d5j5lh41t7oa59nal33qnnnt0@group.calendar.google.com",
    email="reception@ucs.cam.ac.uk",
    )
    
c4breakout.save()

CrateOwner(crate=c4breakout, instid='UIS').save()

CrateAttribute(crate=c4breakout,attribute_type=size, attribute_int=18).save()

Rule(crate = c4breakout, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'cbs.ALL', ).save()
Rule(crate = c4breakout, permission = Permission.objects.get(name='Viewer'), instid = 'CS',).save()
Rule(crate = c4breakout, permission = Permission.objects.get(name='Admin'), groupid='101603',).save()

