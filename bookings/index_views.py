
# CBS Homepage

from django.views.generic import TemplateView

from .models import Crate, Recents, get_recents, Site

# CamConnect calls IBIS web interface, get username, insts for current user
from .cam_connect import CamConnect

class IndexView(TemplateView):
    template_name = 'bookings/index.html'
    
    def get_context_data(self, **kwargs):
        # set up 'context' for template
        context = super(IndexView, self).get_context_data(**kwargs)
        
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
        
        # put 'recent crates' in template context
        recent_crate_ids = get_recents(current_userid)
        recent_crates = []
        for crate_id in recent_crate_ids:
            recent_crates.append(Crate.objects.get(id=crate_id))
        context['recent_crates'] = recent_crates
        
        return context
        
