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
    try:      
        poll = Poll.objects.get(user=username)
    except:
        return render(request, 'poll/index.html', {'error': 'Poll not found'})
    return render(request, 'poll/poll.html', { 'user': username, 'poll': poll })

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
        poll = Poll.objects.get(user=username)
        if poll:
            # Only way to cascade delete all of the Anime objects
            poll.delete()
    except:
        print('Creating poll')
    poll = Poll.objects.create(user=username, list_origin='myanimelist', created=datetime.now())
    mal.save_poll_options(poll, username)
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
    # if voted already, go straight to results
    if username in request.COOKIES:
        try:
            poll = Poll.objects.get(user=username)
            return render(request, 'poll/result.html', { 'user': username, 'poll': poll, 'vote': request.COOKIES[username] })
        except:
            return render(request, 'poll/index.html', {'error': 'Poll not found'})

    a_id = ''
    for i in request:
        a_id = json.loads(i)['id']
    if not a_id:
        return JsonResponse({
            'success': False,
            'message': 'ID not supplied'
        }, status=400)
    try:
        poll = Poll.objects.get(user=username)
        print('poll')
        print(poll)
        anime = poll.anime_set.get(a_id=a_id) 
        print('anime')
        print(anime)
        vote_count = int(anime.votes) + 1
        anime.votes = str(vote_count)
        anime.save()
        
        return JsonResponse({
            'success': True,
        })
    except Exception as e:
        print('something went wrong')
        print(e)
        return JsonResponse({
            'success': False,
            'message': 'Invalid ID or anime not found'
        }, status=400)

def result(request, username):
    ''' Render poll results by user '''
    try:      
        poll = Poll.objects.get(user=username)
        #.order_by('-votes')
    except:
        return render(request, 'poll/index.html', {'error': 'Poll not found'})
    return render(request, 'poll/result.html', { 'user': username, 'poll': poll })