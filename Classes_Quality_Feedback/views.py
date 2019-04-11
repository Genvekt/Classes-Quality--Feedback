from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from surveys.forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            return HttpResponse('Please wait until administrator confirms your account')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})
