
# Usage stats

from django.views.generic import TemplateView

# CamConnect calls IBIS web interface, get username, insts for current user
from .cam_connect import CamConnect

from stats import log_stats, uupm, uupd

class StatsView(TemplateView):
    template_name = 'bookings/stats.html'
    
    def get_context_data(self, **kwargs):
        # set up 'context' for template
        context = super(StatsView, self).get_context_data(**kwargs)
        
        # set top-level 'site' value e.g. to allow custom homepage
        # 'site' defines the id of a cbs 'subsystem' i.e. allows customisation for
        # a given group of users
        site_id = self.request.GET.get('site')
        if site_id:
            context['site'] = Site.objects.get(id=site_id)
        
        # get id of current logged-on user
        current_userid = self.request.META['REMOTE_USER']
        # collect user data and put in template context
        c = CamConnect()
        context['cam_userid'] = current_userid
        context['cam_user'] = c.display_name(current_userid)
        # add inst list for current user to context
        insts = c.user_insts(current_userid)
        context['insts'] = insts
        
        instname_list = []
        for inst in insts:
            instname_list.append(inst.instid)
        context['cam_insts'] = instname_list
        
        #DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
        #debug - make users multi-inst for testing
        instname_list.append('CL')
        #DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG
        
        # now log this page access
        log_stats(current_userid,instname_list,self.request.path,'general','stats','UIS')
        
        # OK here's the whole point... load the stats data
        # Unique Users per Month
        context['uupm'] = uupm()
        
        # Unique Users per Day
        context['uupd'] = uupd()
        
        return context

