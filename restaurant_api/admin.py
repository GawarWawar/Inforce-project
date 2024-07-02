from django.contrib import admin

from . import models

class RestaurantAdmin(admin.ModelAdmin):
    ...

class MenuAdmin(admin.ModelAdmin):
    ...

class VoteAdmin(admin.ModelAdmin):
    ...
    
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Menu, MenuAdmin)
admin.site.register(models.Vote, VoteAdmin)