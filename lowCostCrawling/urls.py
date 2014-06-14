from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'lowCostCrawling.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
