
from django import forms
from django.core.exceptions import ValidationError

from .models import Post
from users.models import Member

class SendPostModelForm(forms.ModelForm):
	post_text = forms.CharField(required=False)

	class Meta:
		model = Post
		exclude = ['member', 'movie', 'datetime', 'rate']
		fields = ['post_text']

	def __init__(self, *args, **kwargs):
		super(SendPostModelForm, self).__init__(*args, **kwargs)
		self.fields['post_text'].widget = forms.Textarea(attrs={'placeholder': 'Your point of view ...', 'id': 'comment', 'style': 'padding: 10px; border-radius: 10px;'})


class EditProfileForm(forms.Form):
	first_name = forms.CharField(label='First Name', required=False, max_length=255)
	last_name = forms.CharField(label='Last Name', required=False, max_length=255)
	displayed_name = forms.CharField(label='Displayed Name', required=False, max_length=255)
	bio = forms.CharField(label='Biography', required=False)
	birthday = forms.DateField(label='Birthday', required=False)
	password = forms.CharField(label='Password', required=False)
	confpass = forms.CharField(label='Confirm Password', required=False)
	prof_image = forms.ImageField(
        label='Select an image', widget=forms.FileInput(attrs={'class': 'file-input btn btn-block btn-primary btn-file'}), required=False
    )


	def __init__(self, member, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': member.user.first_name})
		self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': member.user.last_name})
		self.fields['displayed_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': member.displayed_name})
		self.fields['bio'].widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': member.bio})
		self.fields['birthday'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': member.birthday})
		self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
		self.fields['confpass'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
		# self.fields['prof_image'].widget = forms.FileField(attrs={'class': 'file-input btn btn-block btn-primary btn-file'})

	def clean_password(self):
		if len(self.cleaned_data['password']) != 0 and len(self.cleaned_data['password']) < 6:
			raise forms.ValidationError('Password must be at least 6 charchters long.')

		return self.cleaned_data['password']

	def clean(self):
		cleaned_data = super(EditProfileForm, self).clean()
		password = cleaned_data.get('password')
		password2 = cleaned_data.get('confpass')
		if  (password or password2) and password != password2:
			self.add_error('confpass', forms.ValidationError('Entered passwords don\'t match.'))
