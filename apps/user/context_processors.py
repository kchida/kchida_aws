from django.conf import settings
from apps.user.forms import LoginForm, RegisterForm

def login_reg(request):
    """ These forms are used on all pages """
    return {
        'login_url': settings.LOGIN_URL,
        'login_form': LoginForm,
        'register_form': RegisterForm,
    }