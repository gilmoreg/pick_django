from django.shortcuts import render
from controllers import mal
from .models import Poll
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def index(request):
    ''' Render the homepage '''
    return render(request, 'poll/index.html')

@csrf_exempt
def create_poll(request):
    '''
    Create a new poll
    POST body: auth (a btoa HTTP basic auth string representing the user's MAL login)
    '''
    # need error checking
    username = mal.check_mal_credentials(request.POST.get('auth'))
    if not username:
        return render(request, 'poll/index.html', {'error': 'Invalid credentials'})
    poll = Poll(user=username, list_origin='myanimelist', created=datetime.now())
    mal.save_poll_options(poll, username)
    return render(request, 'poll/index.html')
