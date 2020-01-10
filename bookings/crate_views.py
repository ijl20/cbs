
from django.views.generic import ListView, TemplateView

from django import forms
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse

from django.core.urlresolvers import reverse

from cbs_settings import CBS_Settings

from .models import Crate, CrateTree, Booking, Comment, Recents, update_recents, CrateAttribute, CrateAttributeType, CrateOwner

from .cam_cal import CamCal
# CamConnect calls IBIS web interface, get username, insts for current user
from .cam_connect import CamConnect
# CamRules provides the ability to test permissions for current user/resource
from .cam_rules import CamRules
# CamEmail sends the booking via Hermes to the approver
from .cam_email import CamEmail

import pytz
from datetime import datetime, timedelta

import json # for error print of form.errors

from .stats import log_stats, uupd

class CrateListView(ListView):
    model = Crate
    template_name = 'bookings/crate_list.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CrateListView, self).get_context_data(**kwargs)
        # here we have to build the crate_list of crate_tree structures
        crates = Crate.objects.all()
        top_crates = Crate.objects.filter(parent_crate__isnull=True)
        crate_list = []
        for crate in top_crates:
            crate_list.append( CrateTree(crate) )
                
        context['crate_list'] = crate_list
        return context
    
class ShortBookingForm(forms.Form):
    startdate = forms.CharField(max_length=7)
    starttime = forms.CharField(max_length=6)
    duration = forms.CharField(max_length=6)
    name = forms.CharField(max_length=40)
    crate_id = forms.CharField(max_length=30)
    crate_name = forms.CharField(max_length=100)
    calendar_id = forms.CharField(max_length=100)
    pending = forms.CharField(max_length=1)

class CancelBookingForm(forms.Form):
     booking_reference = forms.CharField(max_length=100)
     
class ApproveBookingForm(forms.Form):
     booking_reference = forms.CharField(max_length=100)
     
class CrateDetailView(TemplateView):
    template_name = 'bookings/crate_detail.html'
    
    def get(self, request, *args, **kwargs):
        self.id = kwargs['pk']
        self.crate = Crate.objects.get(id=self.id)
        self.current_userid = self.request.META['REMOTE_USER']
    
        self.rules = CamRules(self.current_userid, self.crate)
        
        # self.permission is the strongest Permission found for current user for this resource
        # self.reason is a helpful string explaining why permission was granted (i.e. which Rule)
        self.permission, self.reason = self.rules.test('FreeBusyViewer')
        
        if (not self.permission):
            return HttpResponseNotFound()
            #return HttpResponse("Rule was False")
        #else:
        #    return HttpResponse(self.rule)
            
        return super(CrateDetailView, self).get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(CrateDetailView, self).get_context_data(**kwargs)
        
        c = CamConnect()
        context['cam_userid'] = self.current_userid
        context['cam_user'] = c.display_name(self.current_userid)

        # update recents
        
        update_recents(self.current_userid, self.crate)
        
        # set target CrateTree for view
        context['crate_tree'] = CrateTree(self.crate)
        # collect parents of this target
        context['parents'] = context['crate_tree'].parents()

        owner_list = []
        # collect inst owners of this crate
        try:
            owner_list = CrateOwner.objects.filter(crate=self.crate)
        except:
            pass
        
        owner_insts = []
        for owner in owner_list:
            owner_insts.append(c.inst(owner.instid))
        context['owner_insts'] = owner_insts
        
        ## choose start date for bookings/request lists as today minus 8 days...
        
        last_week = datetime.now(pytz.utc)-timedelta(days=8)

        #### Set up PENDING BOOKINGS QuerySet ####
        # create list of pending bookings appropriate for current_userid
        # i.e. list all pending bookings if Approve or above, otherwise list 'self' pending bookings
        is_approver = False
        if self.rules.passes(self.permission, 'Approver'):
            # Approver, so show all pending bookings each with Approve/Cancel
            is_approver = True # set flag to be used in Booked Bookings algorithm below
            pending_bookings = Booking.objects.filter(crate_id=self.id, pending=True, start__gt=last_week)
            for b in pending_bookings:
                b.cancel = True
                b.approve = True
            context['pending'] = pending_bookings
        else:
            # Not an Approver, so show only Self (i.e. own) pending bookings
            pending_bookings = Booking.objects.filter(crate_id=self.id, userid=self.current_userid, pending=True, start__gt=last_week)
            # set Cancel flag on all of these own pending bookings (but Self can't approve)
            for b in pending_bookings:
                b.cancel = True
            context['pending'] = pending_bookings
            
        #### Set 'bookings' flag for tab to be drawn with BOOKED BOOKINGS QuerySet ####
        if self.rules.passes(self.permission, 'Viewer'):
            # current_user is a Viewer or higher, so can see all bookings, but not cancel unless Self (i.e. own)
            booked_bookings = Booking.objects.filter(crate_id=self.id, pending=False, start__gt=last_week)
            # This is the only subtle case: display All bookings but only show Cancel on Self bookings
            # set Cancel flag on all of these own bookings (but Self can't approve)
            for b in booked_bookings:
                if is_approver or b.userid == self.current_userid:
                    b.cancel = True
            context['bookings'] = booked_bookings
        else:
            # Not a Viewer, so show only Self (i.e. own) bookings
            booked_bookings = Booking.objects.filter(crate_id=self.id, userid=self.current_userid, pending=False, start__gt=last_week)
            # set Cancel flag on all of these own pending bookings (but Self can't approve)
            for b in booked_bookings:
                b.cancel = True
            context['bookings'] = booked_bookings
            
        comments = Comment.objects.filter(crate_id=self.id)
        #### Set 'comments' context with 'cancel' flags setting depending on user permissions ####
        if self.rules.passes(self.permission, 'Admin'):
            # current_user is a Admin or higher, so can delete all comments
            for comment in comments:
                comment.cancel = True
        else:
            # Not an Admin, so allow cancel only for Self (i.e. own) comments
            # set Cancel flag on all of these own pending bookings (but Self can't approve)
            for comment in comments:
                if comment.userid == self.current_userid:
                    comment.cancel = True
        context['comments'] = comments

        context['form'] = ShortBookingForm()
        
        context['rules'] = self.rules.rules
        
        context['permission'] = self.permission
        
        # set the 'requires_approval' flag so template will show 'Request Booking' rather than 'Book This'
        context['requires_approval'] = not self.rules.passes(self.permission, 'Booker')
        
        # Set 'settings' to allow settings tab to be drawn
        context['settings'] = True
        
        # populate 'calendar_list' with list of crates
        # check for calendar list in querystring, or in crate object
        if self.crate.calendar_list or self.request.GET.get('calendars'):
            crates = []
            calendars = ''
            if self.request.GET.get('calendars'):
                calendars = self.request.GET.get('calendars')
            else:
                calendars = self.crate.calendar_list
            for crate_id in calendars.split(','):
                crates.append(Crate.objects.get(id=crate_id))
            context['calendars'] = calendars.split(',')
            context['calendar_list'] = crates
            
        # look up crate attributes
        attrs = CrateAttribute.objects.filter(crate=self.crate)
        attributes = []
        for attr in attrs:
            if attr.attribute_type.is_integer:
                attr_val = str(attr.attribute_int)
            else:
                attr_val = attr.attribute_string
                
            attributes.append(attr.attribute_type.name + ' ' + attr_val)
           
        context['attributes'] = attributes
        
        # now log this page access
        insts = c.user_insts(self.current_userid)
        
        instname_list = []
        for inst in insts:
            instname_list.append(inst.instid)
        #DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
        #debug - owning instid is hardcoded to UIS !!
        log_stats(self.current_userid,instname_list,self.request.path,'crate',self.id,'UIS')
        #DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
        
        # define tabs
        if self.crate.calendar_id  or self.crate.calendar_list:
            context['calendar_tab'] = True
            
        if self.crate.map_url:
            context['map_tab'] = True
            
        if context['crate_tree'].children:
            context['children_tab'] = True
            
        if self.rules.passes(self.permission, 'Admin') and not context['crate_tree'].children:
            context['stats_tab'] = True
        
        #debug force tabs on
        #context['calendar_tab'] = True
        context['details_tab'] = True
        context['map_tab'] = True
        context['comments_tab'] = True
        context['bookings_tab'] = True
        context['requests_tab'] = True
        context['settings_tab'] = True
        #context['stats_tab'] = True
        
        # debug
        context['cbs_debug'] = ['User ' + self.current_userid,
                                'User Insts (from lookup): ' + str(instname_list),
                                'User given permission ' + self.permission.name,
                                'Reason for this permission level:' + self.reason,
                                'Attributes: ' + ",".join(attributes),
                               ]
        
        return context

    # This post if for the ShortBookingForm
    def post(self, request, *args, **kwargs):
        #if not request.user.is_authenticated():
        #    return HttpResponseForbidden()

        # Check if user has POST data from Refresh Calendar
        if 'refresh_calendar_form' in request.POST:
            calendars = request.POST.getlist('calendars')
            if len(calendars) == 1:
                return HttpResponseRedirect(CBS_Settings.URL_BASE+'/crate/'+calendars[0])
            return HttpResponseRedirect('?calendars='+','.join(calendars))
            #return HttpResponse('Booking for: '+ st)

        # User has POST of booking form
        form = ShortBookingForm(request.POST)
        if form.is_valid():
            # format UTC date/time string for Google Calendar
            
            # add YEAR (no user input allow up to a year ahead)
            
            now_utc = datetime.now(pytz.utc)
            iyear = now_utc.year
            imonth = now_utc.month
            iday = now_utc.day
            
            form_date = datetime.strptime(form.cleaned_data['startdate'], "%d %b")

            if form_date.month < imonth:
                iyear = iyear + 1

            form.cleaned_data['startyear'] = str(iyear)
            
            crate_id = form.cleaned_data['crate_id']
            crate_name = form.cleaned_data['crate_name']
            summary = form.cleaned_data['name']
            userid = request.META['REMOTE_USER']
            
            c = CamConnect()
            user = c.person(userid)
            for a in user.attributes:
                if a.scheme == 'email':
                    user_email = a.value
                    break
            
            pending = form.cleaned_data['pending'] == '1'

            crate = Crate.objects.get(pk=crate_id)
            # read date/time info from form
            user_string  = form.cleaned_data['startyear']
            user_string += ' ' + form.cleaned_data['startdate']
            user_string += ' ' + ("0"+str(form.cleaned_data['starttime']))[-5:]
            start = datetime.strptime(user_string, "%Y %d %b %H:%M")

            # add local timezone info to date/time read from form
            local_tz = pytz.timezone(CBS_Settings.SYSTEM_TIMEZONE)
            
            # convert date/time to UTC zone
            start_utc = local_tz.localize(start).astimezone(pytz.utc)
            
            duration = datetime.strptime(form.cleaned_data['duration'], "%H:%M")
            
            td = timedelta(hours=duration.hour, minutes=duration.minute)
            
            end_utc = start_utc + td
            
            booking = Booking(
                        userid = userid,
                        user_name = user.displayName,
                        user_email = user_email,
                        crate = crate,
                        name = user.displayName + ' (' +summary+')',
                        reference = 'x', # placeholder
                        link = 'x', # placeholder
                        timestamp = datetime.now(pytz.utc),
                        start = start_utc,
                        end = end_utc,
                        cancelled = False,
                        pending = pending
                        )

            c = CamCal(request)
            event = c.book(booking)
            # update this booking with Google event reference, and save()
            booking.reference = event['id']
            booking.link = event['htmlLink'],
            booking.save()

            if booking.pending:
                e = CamEmail()
                e.send_request(booking)
            
            return HttpResponseRedirect('')
            #return HttpResponse('Booking for: '+ st)
        else:
            #return HttpResponseRedirect('')
            return HttpResponse("Form data issue!!! "+request.POST['startdate']+json.dumps(form.errors))

#    def form_valid(self, form):
#        # Here, we would record the user's interest using the message
#        # passed in form.cleaned_data['message']
#        context = self.get_context_data(**kwargs)
#        context['form'] = form
#        context['object'] = self.get_object()
#        return self.render_to_response(context)
#        return super(RoomDetailView, self).form_valid(form)

class CrateStatsView(TemplateView):
    template_name = 'bookings/crate_stats.html'
    
    def get_context_data(self, **kwargs):
        crate_id = kwargs['pk']
        crate = Crate.objects.get(id=crate_id)
        current_userid = self.request.META['REMOTE_USER']
    
        # SECURITY CHECK
        rules = CamRules(current_userid, crate)
        
        # permission is the strongest Permission found for current user for this resource
        # reason is a helpful string explaining why permission was granted (i.e. which Rule)
        permission, reason = rules.test('FreeBusyViewer')
        
        if (not permission):
            return HttpResponseNotFound()
        # SECURITY CHECK COMPLETE    
        
        context = super(CrateStatsView, self).get_context_data(**kwargs)

        c = CamConnect()
        context['cam_userid'] = current_userid
        context['cam_user'] = c.display_name(current_userid)
        # add inst list for current user to context
        insts = c.user_insts(current_userid)
        context['insts'] = insts
        
        instname_list = []
        for inst in insts:
            instname_list.append(inst.instid)

        # set target CrateTree for view
        context['crate_tree'] = CrateTree(crate)
        # collect parents of this target
        context['parents'] = context['crate_tree'].parents()

        
        # now log this page access
        #DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
        #debug - owning instid is hardcoded to UIS !!
        log_stats(current_userid,instname_list,self.request.path,'crate',crate_id,'UIS')
        #DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG

        # get stats unique-user counts for people viewing this crate
        context['uupd'] = uupd(crate_id=crate_id)
        #context['uupm'] = uupm(instid=instid)
        
        # debug
        context['cbs_debug'] = ['User ' + current_userid,
                                'User Insts (from lookup): ' + str(instname_list),
                                'User given permission ' + permission.name,
                                'Reason for this permission level:' + reason,
                               ]
        

        return context
        
