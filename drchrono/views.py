from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from datetime import datetime

import requests
from pytz import timezone


def get_month_day_str(date_str):
	dash_split = date_str.split('-')
	month_and_day = dash_split[1] + '-' + dash_split[2]
	return month_and_day

def split_birthdays(patient_info, user_timezone):

	before = []
	today = []
	after = []
	no_birthdays = []

	todays_date = datetime.now(timezone(user_timezone))

	today_month_day = todays_date.strftime("%m-%d")

	for p in patient_info:
		try:
			birthday_month_day = get_month_day_str(p['date_of_birth'])
			if birthday_month_day == today_month_day:
				today.append(p)
			elif birthday_month_day > today_month_day:
				after.append((birthday_month_day, p))
			else:
				before.append((birthday_month_day, p))
		except:
			no_birthdays.append(p)

	return before, today, after, no_birthdays

def get_patients_data(access_token, user_timezone):
	headers = {
		'Authorization': 'Bearer ' + access_token,
	}

	patients = []
	patients_url = 'https://drchrono.com/api/patients'
	while patients_url:
		data = requests.get(patients_url, headers=headers).json()
		patients.extend(data['results'])
		patients_url = data['next'] # A JSON null on the last page

	before, today, after, no_birthdays = split_birthdays(patients, user_timezone)

   	return sorted(before), today, sorted(after), no_birthdays


def logout(request):
	auth_logout(request)
	return redirect('/login_page')

@login_required(login_url='/login_page')
def index(request):

	user_timezone = request.COOKIES.get('tzname_from_user', 'UTC')

	# getting access token for user
	access_token = request.user.social_auth.get(provider='drchrono').extra_data['access_token']

	# fetching all user's patients information
	before, today, after, no_birthdays = get_patients_data(access_token, user_timezone)
	content = {}
	content['birthdays_before'] = before
	content['birthdays_today'] = today
	content['birthdays_after'] = after
	content['no_birthdays'] = no_birthdays

	return render(request, 'index.html', content)

def login_page(request):
	if request.user.is_authenticated():
		return redirect('/')
	else:
		return render(request, 'login.html')