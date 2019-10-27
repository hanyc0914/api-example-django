from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

import views


urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='setup'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^checkin/$', views.PatientCheckin.as_view(), name='checkin'),
    url(r'^makeappointment/$', views.MakeAppointment.as_view(), name='makeappointment'),
    url(r'^manage_patient/$', views.manage_patient),
    url(r'^manage_doctor/$', views.manage_doctor),
    url(r'^manage_appointment/$', views.manage_appointment),
    url(r'^checkin/check_in$', views.check_in),
    url(r'^checkin/confirm_information$', views.confirm_information),
    url(r'^checkin/update_information$', views.update_information),
]