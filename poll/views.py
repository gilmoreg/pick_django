from django.shortcuts import render
from controllers import mal

def index(request):
    ''' Render the homepage '''
    return render(request, 'poll/index.html')

def create_poll(request):
    '''
    Create a new poll
    POST paramater: auth (a btoa HTTP basic auth string representing the user's MAL login)
    '''
    # need error checking
    ptw_list = mal.get_list(request.POST.get('auth'))
    # this is called by an ajax request, so what do we do?
    # can try to move away from single page, but in this case it is such a small amount of info
    # could be something like /poll/<user>/share
    return render(request, 'poll/index.html', {'ptw_list': ptw_list})
