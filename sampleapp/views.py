from django.shortcuts import render
from django.http import HttpResponse
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
	return render(
		request, 
		'sample_home.html', 
		{
			"name": request.user.first_name if request.user.first_name else request.user.username
		}
	)
