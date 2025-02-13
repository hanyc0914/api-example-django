from django.db import models
from django.utils import timezone

# Add your models here
class Patient(models.Model):
	patient_id = models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	date_of_birth = models.DateField(null=True)
	gender = models.CharField(max_length=10)
	city = models.CharField(max_length=40)
	state = models.CharField(max_length=40)
	address = models.CharField(max_length=40, null=True)
	ssn = models.CharField(max_length=20, null=True)
	cell_phone = models.CharField(max_length=40, null=True)
	email = models.CharField(max_length=20, null=True)
	doctor_id = models.IntegerField(null=True)
	last_app = models.DateField(null=True, blank=True)
	is_checkin = models.BooleanField(default=False)


class Doctor(models.Model):
	"""docstring for Doctor"""
	doctor_id = models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	specialty = models.CharField(max_length=50)
	cell_phone = models.CharField(max_length=20, null=True)
	email = models.CharField(max_length=20, null=True)


class Appointment(models.Model):
	"""docstring for Appointment"""
	apt_id = models.IntegerField(primary_key=True)
	doctor_id = models.IntegerField()
	patient_id = models.IntegerField()
	scheduled_time = models.DateTimeField()
	duration = models.IntegerField()
	status = models.CharField(max_length=20, null=True)
	reason = models.CharField(max_length=50, null=True)
	exam_room_id = models.IntegerField()


class Checkin(models.Model):
	apt_id = models.IntegerField()
	patient_id = models.IntegerField()
	doctor_id = models.IntegerField()
	checkin_time = models.DateTimeField(null=True, blank=True)
	receive_time = models.DateTimeField(null=True, blank=True)



class ExamRoom(models.Model):
	exam_room_id = models.IntegerField(primary_key=True)
	office_id = models.IntegerField()
	name = models.CharField(max_length=20)

		