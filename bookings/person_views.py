
from django.views.generic import TemplateView

from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.core.urlresolvers import reverse

from .models import Comment, Booking

from .cam_connect import CamConnect

from .cam_rules import CamRules

class PersonView(TemplateView):
    template_name = 'bookings/person_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)

        userid = context['pk']
        self.current_userid = self.request.META['REMOTE_USER']

        # get an IBIS connection
        c = CamConnect()
        context['cam_userid'] = self.current_userid
        context['cam_user'] = c.display_name(self.current_userid)
        
        # set target person for view
        context['target'] = c.person(userid)
         
        # show bookings if self or super-user
        permission, reason = CamRules(self.current_userid, target_userid=userid).test('Self')
        if (permission):
            context['bookings'] = Booking.objects.filter(userid=userid)
            
        context['comments'] = Comment.objects.filter(userid=userid)
        
        # debug
        debug_info = []
        if (permission):
            debug_info = [permission.name]
        debug_info.append(' ' + reason)
        
        context['cbs_debug'] = debug_info
        
        return context
        
