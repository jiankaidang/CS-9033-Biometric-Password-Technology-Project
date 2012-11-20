# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from banksite.models import User
import json

def login_page(request):
    return render_to_response('banksite/login.html', context_instance=RequestContext(request))


def check_user(request):
    post = request.POST
    try:
        user = User.objects.get(uid=post['uid'])
    except (Exception):
        return {
            'success': False,
            'msg': 'The User ID you entered is not correct.'
        }
    else:
        if user.password != post['password']:
            return {
                'success': False,
                'msg': 'The Password you entered is not correct.'
            }
        return {
            'success': True
        }


def login_check(request):
    return HttpResponse(json.dumps(check_user(request)), mimetype='application/json')


def login(request):
    check_result = check_user(request)
    if not check_result['success']:
        raise Http404
    uid = request.POST['uid']
    request.session['uid'] = uid
    return render_to_response('banksite/account.html', {'uid': uid}, context_instance=RequestContext(request))