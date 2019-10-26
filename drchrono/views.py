from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from social_django.models import UserSocialAuth

from drchrono.endpoints import DoctorEndpoint, PatientEndpoint, AppointmentEndpoint, ExamRoomEndpoint
from . import models


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'kiosk_setup.html'


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_welcome.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        api = DoctorEndpoint(access_token)
        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        kwargs['doctor'] = doctor_details
        return kwargs


class PatientCheckin(TemplateView):
    template_name= 'patient_checkin.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        api = PatientEndpoint(access_token)
        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())

    def get_context_data(self, **kwargs):
        kwargs = super(PatientCheckin, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        #patient_details = []
        #for x in self.make_api_request():
        #    patient_details.append(x)
        patient_details = self.make_api_request
        kwargs['patient'] = patient_details
        return kwargs


def manage_patient(request):
    if request.method == 'POST':
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        api = PatientEndpoint(access_token)
        for p in api.list():
            patient = models.Patient(patient_id=p[u'id'], first_name=p[u'first_name'], last_name=p[u'last_name'], \
                                     date_of_birth=p[u'date_of_birth'], gender=p[u'gender'], address=p[u'address'], \
                                     ssn=p[u'social_security_number'], cell_phone=p[u'cell_phone'], email=p[u'email'], \
                                     doctor_id=p[u'doctor'], last_app=p[u'date_of_first_appointment'], is_checkin=False)
            patient.save()
    else:
        pass
    patient_db = models.Patient.objects.all()
    return render(request, 'patient_checkin.html', {})


def manage_doctor(request):
    if request.method == 'POST':
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        api = DoctorEndpoint(access_token)
        for p in api.list():
            doctor = models.Doctor(doctor_id=p[u'id'], first_name=p[u'first_name'], last_name=p[u'last_name'], \
                                   specialty=p[u'specialty'], cell_phone=p[u'cell_phone'], email=p[u'email'])
            doctor.save()
    else:
        pass
    doctor_db = models.Doctor.objects.all()
    return render(request, 'patient_checkin.html', {})


def manage_appointment(request):
    if request.method == 'POST':
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        api = AppointmentEndpoint(access_token)
        for p in api.list(start='2019-10-22', end='2019-10-23'):
            appointment = models.Appointment(apt_id=p[u'id'], doctor_id=p[u'doctor'], patient_id=p[u'patient'], \
                                             scheduled_time=p[u'scheduled_time'], duration=p[u'duration'], \
                                             status=p[u'status'], reason=p[u'reason'], exam_room_id=p[u'exam_room'])
            appointment.save()
    else:
        pass
    appointment_db = models.Appointment.objects.all()
    return render(request, 'patient_checkin.html', {})


def manage_exam_room(request):
    if request.method == 'POST':
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        api = AppointmentEndpoint(access_token)
        for p in api.list(start='2019-10-25', end='2019-10-26'):
            appointment = models.Appointment(apt_id=p[u'id'], doctor_id=p[u'doctor'], patient_id=p[u'patient'], \
                                             scheduled_time=p[u'scheduled_time'], duration=p[u'duration'], \
                                             status=p[u'status'], reason=p[u'reason'], exam_room_id=p[u'exam_room'])
            appointment.save()
    else:
        pass
    appointment_db = models.Appointment.objects.all()
    return render(request, 'patient_checkin.html', {})


def check_in(request):
    ssn = request.GET['ssn']
    first_name = request.GET['firstname']
    last_name = request.GET['lastname']

    try:
        patient = models.Patient.objects.get(ssn=ssn, first_name=first_name, last_name=last_name)
        try:
            patient_appointment = models.Appointment.objects.get(patient_id=patient.patient_id)
            patient.is_checkin = True
            patient.save()
        except ObjectDoesNotExist:
            print('appointment does not exist')
    except ObjectDoesNotExist:
        print('patient does not exist')
    return HttpResponse('check_in finished!')
