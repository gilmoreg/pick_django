import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from controllers import mal
from .models import Poll
from datetime import datetime

def index(request):
    ''' Render the homepage '''
    return render(request, 'poll/index.html')

@csrf_exempt
def create_poll(request):
    '''
    Create a new poll
    POST body: auth (a btoa HTTP basic auth string representing the user's MAL login)
    '''
    username = ''
    for i in request:
        auth = json.loads(i)['auth']
        if auth:
            username = mal.check_mal_credentials(auth)
    if not username:
        return render(request, 'poll/index.html', {'error': 'Invalid credentials'})
    poll = Poll(user=username, list_origin='myanimelist', created=datetime.now())
    mal.save_poll_options(poll, username)
    print poll
    return JsonResponse({
        'success': True,
        'user': username
    })
