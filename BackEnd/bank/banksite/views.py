# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from banksite.models import User
import json

def home(request):
    return render_to_response('banksite/login.html', context_instance=RequestContext(request))


def login(request):
    post = request.POST
    try:
        user = get_object_or_404(User, pk=post['uid'])
    except (KeyError, User.DoesNotExist):
        return HttpResponse(json.dumps({
            'success': False,
            'msg': 'The User ID you entered is not correct.'
        }), mimetype='application/json')
    else:
        if user.password != post['password']:
            return HttpResponse(json.dumps({
                'success': False,
                'msg': 'The Password you entered is not correct.'
            }), mimetype='application/json')
        return HttpResponse(json.dumps({
            'success': True
        }), mimetype='application/json')