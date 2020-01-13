# Run via:
# python manage.py shell
# >>> execfile('setup.py')

####################################################################################
##################### setup_wgb.py          ############################################
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
from bookings.models import *

room = CrateType.objects.get(name="Room")

building = CrateType.objects.get(name="Building")

size = CrateAttributeType.objects.get(id="size")


####################################################################################
####################### Startup data for this system instance ######################
####################################################################################
print('Creating Crates')

wgb = Crate(id="wgb",
    crate_type=building,
    #parent_crate=wcs,
    short_name="William GatesBuilding",
    name="William Gates Building",
    map_url="https://map.cam.ac.uk/William+Gates+Building",
    description="Home of the Computer Laboratory",
    location="On West Cambridge Site, JJ Thomson Avenue",
    calendar_list="",
    email="reception@cl.cam.ac.uk",
    image_list="rnb_1.png",
    )

wgb.save()

####################################################################################
print('Adding crate owners')

CrateOwner(crate=wgb, instid='CL').save()

####################################################################################
print('Adding access permission rules for current crates')

Rule(crate = wgb, permission = Permission.objects.get(name='FreeBusyViewer'), userid = 'ijl20',).save()
Rule(crate = wgb, permission = Permission.objects.get(name='Viewer'), instid = 'CL',).save()
Rule(crate = wgb, permission = Permission.objects.get(name='Admin'), userid='ijl20',).save()

