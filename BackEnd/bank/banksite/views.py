# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from banksite.models import User
import json
import websocket

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
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    response = redirect('accounts')
    response.set_signed_cookie("uid", uid)
    return response


def accounts(request):
    uid = request.session['uid']
    user = User.objects.get(uid=uid)
    return render_to_response('banksite/accounts.html', {'uid': uid, 'service_uid': user.id},
        context_instance=RequestContext(request))


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    response = redirect('login_page')
    response.delete_cookie('uid')
    return response


def signpass_login(request):
    post = request.POST
    service_uid = post['service_uid']
    user = User.objects.get(uid=service_uid)
    service_name = 'chase'
    ws = websocket.create_connection(
        "ws://192.168.0.13:8000/signpass/" + service_name + "/" + user.id + "/serviceLogin")
    ws.send()
    print("socket")
    result = ws.recv()
    ws.close()