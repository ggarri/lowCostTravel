from coreBundle.models.Airport import Airport
from coreBundle.models.AirportCode import AirportCode
from coreBundle.models.Country import Country
from coreBundle.models.Flight import Flight
from django.contrib import admin


# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    model = Flight
    list_filter = ['airport_in', 'airport_out']


# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    model = Country


# Register your models here.
class AirportAdmin(admin.ModelAdmin):
    model = Airport


# Register your models here.
class AirportCodeAdmin(admin.ModelAdmin):
    model = AirportCode

admin.site.register(Flight, FlightAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(AirportCode, AirportCodeAdmin)