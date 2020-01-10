from django.utils.encoding import smart_unicode
from django.db import models

# use json to store recents
import json

# 'CrateType's define hierarchies of types of Crate, e.g. 'Room', 'Building', 'Site'

class CrateType(models.Model):        
    name = models.CharField('Name', max_length=100, blank=True)
    parent_crate_type = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return "Crate type: " + self.name

# 'Crate's are the items that are bookable, or may contain other 'Crates'

class Crate(models.Model):
    id = models.CharField('Crate id', max_length=30, primary_key=True)
    crate_type = models.ForeignKey(CrateType, verbose_name='Type')
    parent_crate = models.ForeignKey('self', blank=True, null=True)
    short_name = models.CharField('Short name (32 max)', max_length=32)
    name = models.CharField('Name', max_length=100)
    map_url =  models.CharField('Link to map', max_length=1000, blank=True, null=True)
    description = models.TextField('Description', max_length=2000, blank=True, null=True)
    location = models.CharField('Location', max_length=100, blank=True, null=True)
    calendar_id = models.CharField('Calendar id', max_length=100, blank=True, null=True)
    calendar_web_color = models.CharField('Calendar web colour', max_length=30, blank=True, null=True)
    calendar_iframe_color = models.CharField('Calendar iframe colour', max_length=30, blank=True, null=True)
    provisional_calendar_id = models.CharField('Provisional Calendar id', max_length=100, blank=True, null=True)
    #calendar_html = models.CharField('Calendar embed html', max_length=1024, blank=True)
    calendar_link = models.CharField('Link to Calendar', max_length=1024, blank=True, null=True)
    email = models.CharField('Email for Approvals', max_length=60, blank=True, null=True)
    calendar_list = models.CharField('Comma separated list of Crate ids for multiple calendars', max_length=300, blank=True, null=True)
    calendar_list_html = models.CharField('Google iframe for multiple calendars', max_length=2000, blank=True, null=True)
    image_list = models.CharField('Comma separated list of image filenames', max_length=300, blank=True, null=True)
    
    def __unicode__(self):
        return "Crate: " + self.name

class CrateOwner(models.Model):
    crate = models.ForeignKey(Crate, verbose_name='Crate id')
    instid = models.CharField('Institution id', max_length=15)
    
    def __unicode__(self):
        return self.crate.id+":"+self.instid
        
# A simple list of permission types, used by Rule above
class Permission(models.Model):
    name = models.CharField('Permission name', max_length=32)
    description = models.TextField('Description', max_length=1024)
    index = models.PositiveIntegerField('Permission precendence (1 is highest)')
    
    def __unicode__(self):
        return self.name

# 'Rule's can be checked to confirm permission current user has for current crate
# e.g. 'Admin', 'View', 'Book', 'RepeatBook', 'Approve'

class Rule(models.Model):
    crate = models.ForeignKey(Crate, verbose_name='Crate id')
    permission = models.ForeignKey(Permission, verbose_name='Permission')
    instid = models.CharField('Inst id', max_length=16, blank=True, null=True)
    userid = models.CharField('CRSid', max_length=16, blank=True, null=True)
    groupid = models.CharField('Group id', max_length=16, blank=True, null=True)

    def __unicode__(self):
        return 'Rule for crate: ' + self.crate.id

class Reference(models.Model):
    crate = models.ForeignKey(Crate, verbose_name='Crate id')
    keyname = models.CharField('Other system key *name* (e.g. PlanOn id)', max_length=16, blank=False)
    keyvalue = models.CharField('Other system reference *value* (i.e. room id)', max_length=30, blank=False)

    def __unicode__(self):
        return self.crate.id + '['+self.keyname+','+self.keyvalue+']'

# 'Comments' can be associated with 'Crates', e.g. a 'Room' could have a noticeboard
class Comment(models.Model):
    crate = models.ForeignKey(Crate, verbose_name='Crate id')
    userid = models.CharField('User id', max_length=50)
    user_name = models.CharField('User name', max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField()
    text = models.TextField('Comment', max_length=1024)
    # index is used to 'pin' the comment at the top of the display list
    index = models.PositiveIntegerField('Index', blank=True, null=True)
    
    def __unicode__(self):
        return 'Comment: '+self.userid+'(' + self.crate.id + ')'

class CrateAttributeType(models.Model):
    id = models.CharField('Type id', max_length=30, primary_key=True)
    crate_type = models.ForeignKey(CrateType, verbose_name='Type')
    name = models.CharField('Name', max_length=100)
    is_integer = models.BooleanField('Is integer')

    def __unicode__(self):
        return '(' + self.crate_type.name + ',' + self.name + ')'

# All crates have the base attributes as per the Crate class
# Plus additional attributes can be stored in this class    
class CrateAttribute(models.Model):
    crate = models.ForeignKey(Crate, verbose_name='Crate id')
    attribute_type = models.ForeignKey(CrateAttributeType, verbose_name='Attribute Type')
    attribute_int = models.PositiveIntegerField('Int value', blank=True, null=True)
    attribute_string = models.CharField('Name', max_length=100, blank=True, null=True)

    def __unicode__(self):
        return 'Attribute: (' + self.crate.id + ')'

# Here is where the booking for a crate by a user is stored        
class Booking(models.Model):
    userid = models.CharField('User id', max_length=50)
    user_name = models.CharField('User name', max_length=50)
    user_email = models.CharField('User email', max_length=75, blank=True, null=True)
    crate = models.ForeignKey(Crate, verbose_name='Crate id')
    name = models.CharField('Name', max_length=100)
    timestamp = models.DateTimeField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    reference = models.CharField('Reference', max_length=100, unique=True)
    link = models.CharField('Link', max_length=300, blank=True, null=True)
    cancelled = models.BooleanField('Cancelled', blank=True)
    cancelled_userid = models.CharField('Cancelled userid', max_length=50, blank=True, null=True)
    cancelled_user_name = models.CharField('Cancelled user name', max_length=50, blank=True, null=True)
    cancelled_timestamp = models.DateTimeField(blank=True, null=True)
    approved_userid = models.CharField('Approved userid', max_length=50, blank=True, null=True)
    approved_user_name = models.CharField('Approved user name', max_length=50, blank=True, null=True)
    pending = models.BooleanField('Requiring Approval', blank=True)

    class Meta:
        ordering = ['start']

    def __unicode__(self):
        return 'Booking: (' + self.crate.id + ',' + self.userid + ')'

class BookingType(models.Model):
    id = models.CharField('Type id', max_length=30, primary_key=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    short_name = models.CharField('Short name (32 max)', max_length=32)
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', max_length=2000, blank=True, null=True)
    
    def __unicode__(self):
        return self.id
        
class BookingTypeTree():
    # booking_type - current BookingType
    # parents - ordered list of crates leading to current crate
    # children - list of 'BookingTypeTree's
    def __init__(self,booking_type):
        # set target crate for view
        self.booking_type = booking_type
        self.children = self.build_tree_list(booking_type)

    # return a list of BookingTypeTrees starting from 'type' BookingType
    def build_tree_list(self, type):
        type_children = BookingType.objects.filter(parent_id=type.id)
        children = []
        for type_child in type_children:
            children.append(BookingTypeTree(type_child))
        
        return children
        
    def parents(self):
        # collect parents of this target
        p = []
        parent = self.booking_type.parent
        while parent:
            p.append(parent)
            parent = parent.parent
        
        p.reverse()
        return p

class CrateTree():
    # crate - current Crate
    # parents - ordered list of crates leading to current crate
    # children - list of 'CrateTree's
    def __init__(self,crate):
        # set target crate for view
        self.crate = crate
        self.children = self.build_tree_list(crate)

    # return a list of CrateTrees starting from 'top' crate
    def build_tree_list(self, top):
        top_crates = Crate.objects.filter(parent_crate_id=top.id)
        children = []
        for crate in top_crates:
            children.append(CrateTree(crate))
        
        return children
        
    def parents(self):
        # collect parents of this target
        p = []
        parent = self.crate.parent_crate
        while parent:
            p.append(parent)
            parent = parent.parent_crate
        
        p.reverse()
        return p

# Recents contains the most recent crates viewed by this user
class Recents(models.Model):
    userid = models.CharField('User id', max_length=50, primary_key=True)
    recent_crates_json = models.CharField('Recent crates list JSON', max_length=500)
    
    def __unicode__(self):
        return self.userid + ',' + self.recent_crates_json
        
# update the Recents data for this user
# Recents contains the most recent crates viewed by this user
def update_recents(userid, crate):
    try:
        r = Recents.objects.get(userid=userid)
        recents_list = json.loads(r.recent_crates_json)
    except Recents.DoesNotExist:
        r = Recents(userid, "") 
        recents_list = []
    new_recents_list = [ crate.id ]
    for crate_id in recents_list:
        if len(new_recents_list) < 10 and crate_id != crate.id:
            new_recents_list.append(crate_id)
    r.recent_crates_json = json.dumps(new_recents_list)
    r.save()
    return
    
def get_recents(userid):
    try:
        r = Recents.objects.get(userid=userid)
        return json.loads(r.recent_crates_json)
    except Recents.DoesNotExist:
        return []

# Site defines the 'white-labelled' website details for an apparent instance of CBS
# note this has NOTHING to do with any Site/Building/Room concept
# i.e. a given department can use CBS with certain 'Site' settings and thus have a
# customised view of the application.
class Site(models.Model):
    id = models.CharField('Site id', max_length=16, primary_key=True)
    instid = models.CharField('Inst id', max_length=16) # inst that 'owns' this Site
    app_name = models.TextField('Application name', max_length=1024, blank=True, null=True) # html application name e.g. "Booking System"
    home_title = models.CharField('Site title', max_length=100, blank=True, null=True)
    home_top = models.TextField('Site top html', max_length=4000, blank=True, null=True) # general HTML text for top of homepage
    home_menu = models.TextField('Site menu', max_length=4000, blank=True, null=True) # left menu of homepage
    home_bottom = models.TextField('Site bottom html', max_length=4000, blank=True, null=True) # general HTML for bottom of homepage
    logo_url = models.CharField('Logo http url', max_length=100, blank=True, null=True)
    logo_image = models.CharField('Logo image', max_length=100, blank=True, null=True)
    logo_alt = models.CharField('Logo alt text', max_length=100, blank=True, null=True)
    breadcrumbs = models.TextField('Site breadcrumb html', max_length=1024, blank=True, null=True) # html initial breadcrumbs

    def __unicode__(self):
        return self.id + '(' + self.instid + ')'

# Unique-users-per-month counts separated into their own table
class MonthUsers(models.Model):
    siteid = models.CharField('Site id', max_length=16)
    ref = models.CharField('Reference id', max_length=100) # some reference for this count
    month = models.DateField('Date')
    count = models.PositiveIntegerField('Count')
    
    class Meta:
        ordering = ['month']
        
    def __unicode__(self):
        return unicode(self.siteid) + ' ' + unicode(self.ref) + ' ' + unicode(self.month) + ' ' + unicode(self.count)

# Given the data-driven-web-design, stats can be collected per NOUN (e.g. person, inst, crate)
# Noun types are pre-defined in this table
class NounType(models.Model): # holds general 'resource types' in system we might keep stats on, e.g. crate, user, inst
    id = models.CharField('Type id', max_length=16, primary_key=True) # short key for the resource e.g. crate
    description = models.CharField('Description', max_length=1024, blank=True, null=True) # longer description of resource type
    
    def __unicode__(self):
        return unicode(self.id)

# PageAccess is like a compressed form of the Apache log.
# An entry is created per-user, per-inst, per-page-access
# I.e. a user belonging to two insts will create double the number of entries
# But each entry is UNIQUE-PER-DAY, i.e. the same user accessing the same page multiple times will
# only create a single record.
# This is to support the primary purpose of unique-users stats at a page/primary-noun granularity
class PageAccess(models.Model):
    date = models.DateField('Date') # date this access occurred (only keep unique entries)
    userid = models.CharField('User id', max_length=50) # user that triggered this access
    user_instid = models.CharField('User Inst id', max_length=16) # inst this user belongs to (can have multiple)
    user_instcount = models.PositiveIntegerField('User inst count', blank=True, null=True); # number of insts for this user
    page_url = models.CharField('Url', max_length=300) # url reference to page e.g. /bookings/crate/Au310
    noun_type = models.ForeignKey(NounType, verbose_name='Page Type') # resource type on page, e.g. crate, inst, user
    noun_id = models.CharField('Resource id', max_length=50) # key for the resource, e.g. userid, instid, crate_id
    noun_instid = models.CharField('Object Inst id', max_length=16) # inst this resource belongs to
    
    class Meta:
        ordering = ['date']
        
    def __unicode__(self):
        return (unicode(self.date) +' ('+ 
               unicode(self.userid) +' of '+ unicode(self.user_instid)  + '/'+
               unicode(self.user_instcount) + ') ('+
               unicode(self.noun_type.id) +' '+ unicode(self.noun_id) +') '+
               unicode(self.page_url))

# Per DAY, one record of this type is created per-user per-institution
# i.e. if user belongs to 2 insts, there will be 2 records per day 
class UserAccess(models.Model):
    date = models.DateField('Date') # date this access occurred (only keep unique entries)
    userid = models.CharField('User id', max_length=50) # user that triggered this access
    user_instid = models.CharField('User Inst id', max_length=16) # inst this user belongs to (can have multiple)
    user_instcount = models.PositiveIntegerField('User inst count', blank=True, null=True); # number of insts for this user
    
    class Meta:
        ordering = ['date']
        
    def __unicode__(self):
        return (unicode(self.date) +' '+ 
               unicode(self.userid) +' of '+ unicode(self.user_instid) + '/'+
               unicode(self.user_instcount))
    
    