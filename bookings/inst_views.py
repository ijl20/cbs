
from django.views.generic import TemplateView

from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.core.urlresolvers import reverse

from .models import Comment, Booking, CrateOwner

from .cam_connect import CamConnect

from .stats_views import log_stats, uupd, uupm

class InstView(TemplateView):
    template_name = 'bookings/inst_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(InstView, self).get_context_data(**kwargs)

        instid = context['pk']

        # collect user data and put in template context
        # get id of current logged-on user
        current_userid = self.request.META['REMOTE_USER']
        c = CamConnect()
        context['cam_userid'] = current_userid
        context['cam_user'] = c.display_name(current_userid)
        # add inst list for current user to context
        insts = c.user_insts(current_userid)
        context['insts'] = insts
        
        instname_list = []
        for inst in insts:
            instname_list.append(inst.instid)

        # set target person for view
        context['target'] = c.inst(instid)
        
        owned_crates_list = CrateOwner.objects.filter(instid=instid)
        bookings = []
        comments = []
        crates = []
        for crate_owner in owned_crates_list:
            bookings_for_this_crate = Booking.objects.filter(crate_id=crate_owner.crate.id)
            bookings.append(bookings_for_this_crate)
            comments_for_this_crate = Comment.objects.filter(crate_id=crate_owner.crate.id)
            comments.append(comments_for_this_crate)
            crates.append(crate_owner.crate)
                
        # put these lists into the page context
        context['bookings'] = bookings
        context['comments'] = comments
        context['crates'] = crates
        
        # now log this page access
        log_stats(current_userid,instname_list,self.request.path,'inst',instid,instid)

        return context
        
class InstStatsView(TemplateView):
    template_name = 'bookings/inst_stats.html'
    
    def get_context_data(self, **kwargs):
        context = super(InstStatsView, self).get_context_data(**kwargs)

        instid = context['pk']

        # collect user data and put in template context
        # get id of current logged-on user
        current_userid = self.request.META['REMOTE_USER']
        c = CamConnect()
        context['cam_userid'] = current_userid
        context['cam_user'] = c.display_name(current_userid)
        # add inst list for current user to context
        insts = c.user_insts(current_userid)
        context['insts'] = insts
        
        instname_list = []
        for inst in insts:
            instname_list.append(inst.instid)

        # set target person for view
        context['target'] = c.inst(instid)
        
        # now log this page access
        log_stats(current_userid,instname_list,self.request.path,'inst',instid,instid)

        # get stats unique-user counts for people from this inst
        context['uupd'] = uupd(instid=instid)
        context['uupm'] = uupm(instid=instid)
        return context
        
class InstListView(TemplateView):
    template_name = 'bookings/inst_list.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InstListView, self).get_context_data(**kwargs)
        # here we have to build the crate_list of crate_tree structures
        instid_tuples = CrateOwner.objects.values('instid').distinct()
        # get an IBIS connection
        c = CamConnect()
        instids = []
        for instid in instid_tuples:
            instids.append(instid['instid'])
        insts = c.insts(instids)
                
        context['insts'] = insts
        return context
    
