from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

USER_MODEL = get_user_model()
EXISTING_EMAIL_ERROR_MESSAGE = 'User with this email already exists.'


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = USER_MODEL
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def clean_email(self) -> str | None:
        """
        Validation function to check the uniqueness of emails.

        :raise: forms.ValidationError
        :return: if correct - new email, otherwise raise forms.ValidationError
        """
        new_email: str = self.cleaned_data['email']

        try:
            if USER_MODEL.objects.get(email=new_email):
                raise forms.ValidationError(EXISTING_EMAIL_ERROR_MESSAGE)
        except USER_MODEL.DoesNotExist:
            return new_email
