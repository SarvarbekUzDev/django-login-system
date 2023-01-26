from django import forms

from .models import CustomUser


class CustomUserForm(forms.ModelForm):
	username = forms.CharField(label="Username" , max_length=150, help_text="Required. 150 characters or fewer")
	email = forms.EmailField(label="Email" , max_length=150)
	password = forms.CharField(label="Password",
			strip=False,
			widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),)
	class Meta:
		model = CustomUser
		fields = ('username','email','password',)

	def save(self, commit=True):
		user = super().save(commit)
		user.set_password(self.cleaned_data['password'])
		user.save()

		return user
