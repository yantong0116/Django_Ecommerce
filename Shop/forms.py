from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Member


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Member
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Member
        fields = ('email',)
