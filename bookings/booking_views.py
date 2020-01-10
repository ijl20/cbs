
from django.views.generic import TemplateView

from django import forms

from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseNotFound


from .models import Booking,BookingType,BookingTypeTree

from .cam_cal import CamCal
# CamEmail sends approve/cancel notifications via Hermes to the event creator
from .cam_email import CamEmail
# CamConnect calls IBIS web interface, get username, insts for current user
from .cam_connect import CamConnect

import pytz
from datetime import datetime

class BookingActionForm(forms.Form):
    action = forms.CharField(max_length=30)
     
class BookingView(TemplateView):
    template_name = 'bookings/booking_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookingView, self).get_context_data(**kwargs)
        reference = context['pk']
        # set target crate for view
        context['booking'] = Booking.objects.get(reference=reference)
        
        return context
        
    def post(self, request, *args, **kwargs):
        #if not request.user.is_authenticated():
        #    return HttpResponseForbidden()
        form = BookingActionForm(request.POST)
        reference = kwargs['pk']
        if form.is_valid():
            # format UTC date/time string for Google Calendar
            
            # add YEAR (no user input allow up to a year ahead)
            
            now_utc = datetime.now(pytz.utc)
            
            cbs_debug = 'BookingView post '
            if form.cleaned_data['action'] == 'CANCEL':
                booking = Booking.objects.get(reference__exact=reference)
                cbs_debug = 'BookingView CANCEL '+ booking.name
                c = CamCal(request)
                c.cancel(booking)
                e = CamEmail()
                e.send_cancellation(booking)

                
            elif form.cleaned_data['action'] == 'APPROVE':
                booking = Booking.objects.get(reference__exact=reference)
                cbs_debug = 'BookingView APPROVE '+ booking.name
                c = CamCal(request)
                c.cancel(booking)
                booking.pending = False
                event = c.book(booking)
                booking.reference = event['id']
                booking.link = event['htmlLink'],
                booking.save()
                e = CamEmail()
                e.send_approval(booking)
                
            return HttpResponseRedirect('../../crate/%s/' % booking.crate.id)
            # debug return
            cbs_debug += ' REMOTE_USER=' + request.META['REMOTE_USER']
            cbs_debug += ' action=' + form.cleaned_data['action']
            cbs_debug += ' reference=' + reference
            return HttpResponse(cbs_debug)
        else:
            return HttpResponse("Form data issue!!! "+reference)

# This class sets context with tree of booking types
class BookingTypesViewX(TemplateView):
    template_name = 'bookings/booking_types.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookingTypesView, self).get_context_data(**kwargs)
        current_userid = self.request.META['REMOTE_USER']
        c = CamConnect()
        context['cam_userid'] = current_userid
        context['cam_user'] = c.display_name(current_userid)

        # set target BookingTypeTree for view
        context['booking_type_tree'] = BookingTypeTree(root_type)
                    
        # debug
        context['debug'] = "ABC"
        
        return context
        
# This class sets context with tree of booking types
class BookingTypesView(TemplateView):
    template_name = 'bookings/booking_types.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookingTypesView, self).get_context_data(**kwargs)
                    
        current_userid = self.request.META['REMOTE_USER']
        c = CamConnect()
        context['cam_userid'] = current_userid
        context['cam_user'] = c.display_name(current_userid)

        try:
            root_type = BookingType.objects.get(id=kwargs['pk'])
        except:
            return HttpResponseNotFound()
            
        # set target BookingTypeTree for view
        context['booking_type_tree'] = BookingTypeTree(root_type)
                    
        return context
        
 