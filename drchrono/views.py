from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required



def logout(request):
	auth_logout(request)
	return redirect('/login_page')

@login_required(login_url='/login_page')
def index(request):
	return render(request, 'index.html')

def login_page(request):
	if request.user.is_authenticated():
		return redirect('/')
	else:
		return render(request, 'login.html')