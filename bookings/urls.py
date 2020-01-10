from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from bookings.index_views import IndexView
from bookings.crate_views import CrateDetailView, CrateListView, CrateStatsView
from bookings.person_views import PersonView
from bookings.inst_views import InstView, InstListView, InstStatsView
from bookings.booking_views import BookingView, BookingTypesView
from bookings.comment_views import CommentView
from bookings.stats_views import StatsView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^crate/(?P<pk>[-_\w]+)/$', CrateDetailView.as_view(), name='crate'),
    url(r'^crate_stats/(?P<pk>[-_\w]+)/$', CrateStatsView.as_view(), name='crate_stats'),
    url(r'^crates/$', CrateListView.as_view(), name='crates'),
    url(r'^person/(?P<pk>[-_\w]+)/$', PersonView.as_view(), name='person'),
    url(r'^inst/(?P<pk>[-_\w]+)/$', InstView.as_view(), name='inst'),
    url(r'^inst_stats/(?P<pk>[-_\w]+)/$', InstStatsView.as_view(), name='inst_stats'),
    url(r'^insts/$', InstListView.as_view(), name='insts'),
    #url(r'^booking/$', BookingView.as_view(), name='booking'),
    url(r'^booking/(?P<pk>[-_\w]+)/$', BookingView.as_view(), name='booking'),
    url(r'^booking_types/(?P<pk>[-_\w]+)/$', BookingTypesView.as_view(), name='booking_types'),
    #url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^comment/(?P<pk>[-_\w]+)/$', CommentView.as_view(), name='comment'),
    # static information pages
    url(r'^about$', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^help$', TemplateView.as_view(template_name='help.html'), name="help"),
    url(r'^stats$', StatsView.as_view(), name="stats"),
    )