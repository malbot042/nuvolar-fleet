from django.contrib import admin

from fleet.models import Airport, Aircraft, Flight


admin.site.register(Airport)
admin.site.register(Aircraft)
admin.site.register(Flight)
