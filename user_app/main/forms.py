from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.disallow_usernames = ('admin', 'administrator', 'moderator', 'mod')

    class Meta:
        model = MyUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean(self):
        super().clean()
        if self.cleaned_data.get("username").lower().startswith(self.disallow_usernames):
            raise ValidationError(
                f'Nazwy użytkownika rozpoczynające się od {self.disallow_usernames} są zarezerwowane dla administracji'
            )

