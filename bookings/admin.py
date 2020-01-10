from django.contrib import admin
from .models import *

admin.site.register(Crate)
admin.site.register(CrateType)
admin.site.register(Permission)
admin.site.register(Rule)
admin.site.register(Reference)
admin.site.register(Comment)
admin.site.register(CrateAttributeType)
admin.site.register(CrateAttribute)
admin.site.register(Booking)
admin.site.register(CrateOwner)
admin.site.register(Recents)

