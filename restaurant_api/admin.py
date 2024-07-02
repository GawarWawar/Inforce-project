from django.contrib import admin

from . import models

class RestourantAdmin(admin.ModelAdmin):
    ...

class MenuAdmin(admin.ModelAdmin):
    ...

class VoteAdmin(admin.ModelAdmin):
    ...
    
admin.site.register(models.Restourant, RestourantAdmin)
admin.site.register(models.Menu, MenuAdmin)
admin.site.register(models.Vote, VoteAdmin)