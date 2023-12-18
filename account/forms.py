from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User
from dtks.models import Kecamatan

class CreateUserForm(UserCreationForm):
	kecamatan_choices = [('','--Pilih Kecamatan--'),]
	for i in Kecamatan.objects.all().order_by('nama_kecamatan'):
		kecamatan_choices.append((i.nama_kecamatan,i.nama_kecamatan))
	
	location = forms.ChoiceField(choices=kecamatan_choices)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["name"].widget.attrs.update({
			'type': 'text',
			'class':'form-control',
			'id':'name',
			'name':'name',
			'required': ''
		})
		self.fields["username"].widget.attrs.update({
			'type': 'text',
			'class':'form-control',
			'id':'location',
			'name':'location',
			'required': '',
			'minlength':'5',
			'maxlength':'15'
		})
		self.fields["password1"].widget.attrs.update({
			'type': 'password',
			'class':'form-control',
			'id':'password1',
			'name':'password1',
			'required': ''
		})
		self.fields["password2"].widget.attrs.update({
			'type': 'password',
			'class':'form-control',
			'id':'password2',
			'name':'password2',
			'required': ''
		})
		self.fields["location"].widget.attrs.update({
			'type': 'text',
			'class':'form-control',
			'id':'location',
			'name':'location',
			'required': ''
		})
	class Meta:
		model = User
		fields = ['name', 'username', 'password1', 'password2', 'location']


class ChangePasswordForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for fieldname in ['old_password', 'new_password1', 'new_password2']:
			self.fields[fieldname].widget.attrs.update({'class':'form-control'})