from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name',)
        # exclude = ()


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')
