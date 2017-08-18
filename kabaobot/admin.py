from django.contrib import admin
from .models import *

# Register your models here.
class EntryAdmin(admin.ModelAdmin)
    pass

class LineUserAdmin(admin.ModelAdmin)
    pass

admin.site.register(Entry, EntryAdmin)
admin.site.register(LineUser, LineUserAdmin)

