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

def poll(request, username):
    ''' Render a poll by user '''
    poll_object = Poll.objects.get(user=username)
    print(poll_object)
    anime = {
        'title': 'test',
        'image': 'test',
        'anime_id': '123'
    }
    poll = {
        'anime_list': [ anime ]
    }
    return render(request, 'poll/poll.html', { 'user': 'pickdemo', 'poll': poll })

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
    poll.save()
    mal.save_poll_options(poll, username)
    print poll
    return JsonResponse({
        'success': True,
        'user': username
    })
