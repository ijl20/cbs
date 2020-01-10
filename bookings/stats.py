# Stats support classes

from datetime import date

from django.db.models import Count, Min, Max

from .models import MonthUsers, NounType, PageAccess, UserAccess

################################################################################
#  log_stats
################################################################################
# userid: user id of user that requested the page
# user_insts: list of instid's that user belongs to
# url: some reference to the page accessed, e.g. /bookings/crate/Au311
# noun_type: type of object accessed, e.g. crate, person, inst
# noun_id: id of object accessed, e.g. Au311, ijl20
# noun_owner: instid that owns the object, e.g. CS owns Au311
def log_stats(userid, user_insts, url, noun_type, noun_id, noun_owner):
    today = date.today()

    # store UserAccess record for later unique-users stats
    for user_inst in user_insts: # one record per user/inst per day
        try:
            UserAccess.objects.get(date=today, userid=userid, user_instid=user_inst)
        except UserAccess.DoesNotExist:
            UserAccess( date=today, userid=userid, user_instid=user_inst, user_instcount=len(user_insts)).save()

    # now store a pageaccess record for each of the user insts
    # convert string 'noun_type' into a NounType object
    nt = NounType.objects.get(id=noun_type)
    for user_inst in user_insts:
        try:
            PageAccess.objects.get(date=today, userid=userid, user_instid=user_inst, user_instcount=len(user_insts), 
                                   page_url=url, noun_type=nt, noun_id=noun_id, noun_instid=noun_owner)
        except PageAccess.DoesNotExist:
            PageAccess( date=today, userid=userid, user_instid=user_inst, user_instcount=len(user_insts), 
                                   page_url=url, noun_type=nt, noun_id=noun_id, noun_instid=noun_owner).save()

################################################################################
#  get_uupd_data - Unique Users Per Day
################################################################################
# data is calculated from UserAccess objects
# An instid is option, if present only users with that instid will be counted
def uupd(instid=None, crate_id=None):
    uupd = []
    series = { 'label': 'unique users per day' }
    stats = []
    if instid is None and crate_id is None:
        stats = UserAccess.objects.values_list('date').annotate(users=Count('userid',distinct=True))
    elif not instid is None:
        stats = UserAccess.objects.filter(user_instid__exact=instid).values_list('date').annotate(users=Count('userid',distinct=True))
    elif not crate_id is None:
        nt_crate = NounType.objects.get(id='crate')
        stats = PageAccess.objects.filter(noun_type__exact=nt_crate, noun_id__exact=crate_id).values_list('date').annotate(users=Count('userid',distinct=True))
    series['stats'] = stats
    uupd.append(series)
    return uupd
    
################################################################################
#  get_uupm_data - Unique Users Per Month
################################################################################
# data is calculated from UserAccess objects
# returns a list of multiple series [{ label: "xxx", stats: [(date, count),...] },...]
def uupm(instid=None,crate_id=None):
    uupm = []
    series = { 'label': 'unique users per month' }
    stats = [] # MonthUsers.objects.values_list('month','count')

    if instid is None:
        start_date = UserAccess.objects.aggregate(Min('date'))['date__min']
    else:
        start_date = UserAccess.objects.filter(user_instid__exact=instid).aggregate(Min('date'))['date__min']

    finish_date = UserAccess.objects.aggregate(Max('date'))['date__max']

    current_date = date(start_date.year, start_date.month, 1)
    while current_date < finish_date:
        end_year = current_date.year
        end_month = current_date.month + 1
        if end_month == 13:
            end_month = 1
            end_year = end_year + 1
        end_date = date(end_year, end_month, 1)
        if instid is None:
            count = UserAccess.objects.filter(date__gte=current_date, date__lt=end_date).values('userid').distinct().count()
        else:
            count = UserAccess.objects.filter(user_instid__exact=instid,date__gte=current_date, date__lt=end_date).values('userid').distinct().count()
        stats.append((current_date, count))
        current_date = end_date

    series['stats'] = stats
    uupm.append(series)

    return uupm

