from coreBundle.models import *
from django.contrib import admin


# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    model = Flight
    list_filter = ['edreams_geoId_in', 'edreams_geoId_out']

# Register your models here.
class CountryAdmin(admin.ModelAdmin):
	model = Country

# Register your models here.
class AirportAdmin(admin.ModelAdmin):
	model = Airport

admin.site.register(Flight, FlightAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Airport, AirportAdmin)