from django.contrib import admin

from pickupyou.schedule.models import Coordinates, Driver, Order


class OrderAdmin(admin.ModelAdmin):
    list_filter = ("start_time", "day")
    ordering = ["day"]


class DriverAdmin(admin.ModelAdmin):
    ordering = ["first_name"]


admin.site.register(Coordinates)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Order, OrderAdmin)
