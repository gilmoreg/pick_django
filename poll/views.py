''' Django Views '''
import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from poll.controllers import mal
from poll.models import Poll

def index(request):
    ''' Render the homepage '''
    return render(request, 'poll/index.html')

def poll(request, username):
    ''' Render a poll by user '''
    try:
        get_poll = Poll.objects.get(user=username)
        # if voted already, go straight to results
        if username in request.COOKIES:
            return render(request, 'poll/result.html',
                          {'user': username,
                           'poll': get_poll,
                           'vote': request.COOKIES[username]})
    except Exception as e:
        print(e)
        return render(request, 'poll/index.html', {'error': 'Poll not found'})
    return render(request, 'poll/poll.html', {'user': username, 'poll': get_poll})

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
    try:
        get_poll = Poll.objects.get(user=username)
        if get_poll:
            # Only way to cascade delete all of the Anime objects
            get_poll.delete()
    except Exception as e:
        print('') # do nothing - this just means this is a new poll and not a real error
    get_poll = Poll.objects.create(user=username, list_origin='myanimelist', created=datetime.now())
    mal.save_poll_options(get_poll, username)
    return JsonResponse({
        'success': True,
        'user': username
    })

@csrf_exempt
def vote(request, username):
    '''
    Vote on a poll
    POST body: id (the id of the anime voted for)
    '''
    a_id = ''
    for i in request:
        a_id = json.loads(i)['id']
    if not a_id:
        return JsonResponse({
            'success': False,
            'message': 'ID not supplied'
        }, status=400)
    try:
        get_poll = Poll.objects.get(user=username)
        anime = get_poll.anime_set.get(a_id=a_id)
        vote_count = int(anime.votes) + 1
        anime.votes = str(vote_count)
        anime.save()
        response = JsonResponse({
            'success': True,
        })
        response.set_cookie(username, anime.a_id)
        return response
    except Exception as e:
        print(e)
        return JsonResponse({
            'success': False,
            'message': 'Invalid ID or anime not found'
        }, status=400)

def result(request, username):
    ''' Render poll results by user '''
    try:
        get_poll = Poll.objects.get(user=username)
        return render(request, 'poll/result.html', {'user': username, 'poll': get_poll})
    except Exception as e:
        print(e)
        return render(request, 'poll/index.html', {'error': 'Poll not found'})
