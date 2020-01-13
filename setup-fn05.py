####################################################################################
print('Adding FN05')

from bookings.models import *

room = CrateType.objects.get(name="Room")

wgb = Crate.objects.get(id="wgb")

size = CrateAttributeType.objects.get(id="size")

## FN05Meeting Room
fn05 = Crate(id="fn05",
    crate_type=room,
    parent_crate=wgb,
    short_name="FN05 Mtg Rm",
    name="Gates Building FN05 Meeting Room",
    map_url="https://map.cam.ac.uk/William+Gates+Building",
    description="A CL meeting room, takes up to 18 people comfortably. This room will be equipped with projector, flat screen, telephone, ability to videoconference (both hardware codec and webconference solutions). It can be booked for any type of meeting including union meetings.",
    location="1st floor William Gates Building",
    calendar_web_color="#914D14",
    calendar_iframe_color="%236B3304",
    calendar_id="cam.ac.uk_0ukhh087prehuj8t11duqq28no@group.calendar.google.com",
    provisional_calendar_id="cam.ac.uk_84ke820r406h1h9vhmeje1lee4@group.calendar.google.com",
    email="reception@ucs.cam.ac.uk",
    )

fn05.save()

CrateOwner(crate=fn05, instid='CL').save()

CrateAttribute(crate=fn05,attribute_type=size, attribute_int=18).save()

Rule(crate = fn05, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'ijl20', ).save()
Rule(crate = fn05, permission = Permission.objects.get(name='Booker'), instid = 'CL',).save()
Rule(crate = fn05, permission = Permission.objects.get(name='Admin'), groupid='101603',).save()

