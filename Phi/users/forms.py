
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError

from .models import Member

class MemberRegModelForm(forms.ModelForm):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)
	password2 = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	captcha = CaptchaField()

	class Meta:
		model = Member
		exclude = ['user', 'followees', 'bio']
		fields = ['username', 'displayed_name', 'password', 'password2', 'email', 'birthday', 'captcha']

	def __init__(self, *args, **kwargs):
		super(MemberRegModelForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
		self.fields['displayed_name'].widget = forms.TextInput(attrs={'placeholder': 'Name to Be Displayed'})
		self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password Again'})
		self.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'Email'})
		self.fields['birthday'].widget = forms.TextInput(attrs={'id': 'datepicker', 'placeholder': 'Birthday'})

	def clean_password(self):
		if len(self.cleaned_data['password']) < 6:
			raise forms.ValidationError('Password must be at least 6 charchters long.')

		return self.cleaned_data['password']

	def clean(self):
		cleaned_data = super(MemberRegModelForm, self).clean()
		password = cleaned_data.get('password')
		password2 = cleaned_data.get('password2')
		if  password and password2 and password != password2:
			self.add_error('password2', forms.ValidationError('Entered passwords don\'t match.'))

class MemberLoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)

	def __init__(self, *args, **kwargs):
		super(MemberLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
		self.fields['registered-username'] = self.fields['username']
		del self.fields['username']
		self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
		self.fields['registered-password'] = self.fields['password']
		del self.fields['password']
