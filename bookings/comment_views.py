
from django.views.generic import TemplateView

from django import forms

from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import HttpResponse


from .models import Crate, Comment

import pytz
from datetime import datetime

class CommentForm(forms.Form):
    text = forms.CharField(max_length=1024, required=False)
    pin = forms.BooleanField(required=False)
    crate_id = forms.CharField(max_length=30, required=False)
    action = forms.CharField(max_length=30)
    user_name = forms.CharField(max_length=50, required=False)

class CommentActionForm(forms.Form):
    action = forms.CharField(max_length=30)
    
class CommentView(TemplateView):
    template_name = 'bookings/comment_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        reference = context['pk']
        # set target crate for view
        context['comment'] = Comment.objects.get(id=reference)
        
        return context
        
    def post(self, request, *args, **kwargs):
        #if not request.user.is_authenticated():
        #    return HttpResponseForbidden()
        form = CommentForm(request.POST)
        if form.is_valid():
            # format UTC date/time string for Google Calendar
            
            # add YEAR (no user input allow up to a year ahead)
            
            now_utc = datetime.now(pytz.utc)
            comment_id = kwargs['pk'] # only valid for CANCEL

            cbs_debug = 'CommentView post '
            if form.cleaned_data['action'] == 'CANCEL':
                comment = Comment.objects.get(id=comment_id)
                comment.delete()
                cbs_debug = 'CommentView CANCEL '+ comment.text
                
            elif form.cleaned_data['action'] == 'APPROVE':
                comment = Comment.objects.get(id=reference)
                cbs_debug = 'CommentView APPROVE '+ comment.user_name
                
            elif form.cleaned_data['action'] == 'ADD':
                index = 0
                if form.cleaned_data['pin']:
                    index = 1
                    
                comment = Comment(
                    crate = Crate.objects.get(id=form.cleaned_data['crate_id']),
                    userid = request.META['REMOTE_USER'],
                    user_name = form.cleaned_data['user_name'],
                    timestamp = now_utc,
                    text = form.cleaned_data['text'],
                    index = index,
                    )
                comment.save()
    
                cbs_debug = 'CommentView ADD '+ comment.user_name
                
            return HttpResponseRedirect('../../crate/%s/#comments' % comment.crate.id)
            # debug return
            cbs_debug += ' REMOTE_USER=' + request.META['REMOTE_USER']
            cbs_debug += ' action=' + form.cleaned_data['action']
            cbs_debug += ' reference=' + str(comment.id)
            return HttpResponse(cbs_debug)
        else:
            return HttpResponse("Form data issue!!! "+reference)
