import random
from django.http import HttpResponse
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
#from django_websocket import require_websocket,accept_websocket

from apns import APNs, Payload

'''check if the username is existing'''

def checkUsername(request, username):
    try:
        User.objects.get(username=username)
        return HttpResponse(json.dumps({'success': 0, 'msg': "username existing"}))
    #    return HttpResponse("Yes")
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'success': 1, 'msg': "username not existing"}))

'''register  username + email + signature into  signpass'''

def register(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username')
            User.objects.get(username=username)
            return HttpResponse(json.dumps({'success': 0, 'msg': "username existing"}))
        except User.DoesNotExist:
            email = request.GET.get('email')
            signature = request.GET.get('signature')
            udid = request.GET.get('udid')
            dev_token = request.GET.get('dev_token')
            print "udid=" + udid
            try:
                user = User.objects.create(username=username, email=email)
                piece = Piece.objects.create(user=user, signature=signature)
                iPhone = IPhone.objects.get(dev_token=dev_token)
                iPhone.piece = piece
                iPhone.udid = udid
                iPhone.save()
                return HttpResponse(json.dumps({'success': 1, 'msg': "%s is created successfully" % username}))
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))

#      except:
#        print sys.exc_info


'''
service side sends a bind request with service_name and service_uid
'''

def bindRequestFromService(request, service_name, service_uid):
    try:
    #    binding=Binding.objects.create(service_name=service_name,service_uid=service_uid)
    #    binding.save()
        return render_to_response("bind.html", {"service_name": service_name, "service_uid": service_uid},
            context_instance=RequestContext(request))
    except Binding.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "binding not existing"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "username not existing"}))
    except Piece.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "Piece not existing"}))
    except Service.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "service %s is not registered" % service_name}))
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))


def bindRequestPoll(request):
    if request.method == "POST":
        service_name = request.POST["service_name"]
        service_uid = request.POST["service_uid"]
    try:
        service = Service.objects.get(service_name=service_name)
        if Binding.objects.get(service=service, service_uid=service_uid):
            return HttpResponse(json.dumps({'success': 1, 'msg': "binding successed"}))
    except Service.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "service %s is not registered" % service_name}))
    except Binding.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "binding is NOT existing"}))


def checkServicename(request, service_name):
    try:
        User.objects.get(service_name=service_name)
        return HttpResponse("s% is existing" % service_name)
    except User.DoesNotExist:
        return HttpResponse("s% is not existing" % service_name)


def find_iOS(binding_id):
    pass


def createVerify(binding):
    Verify.objects.create(binding=binding)


def verifySuccessed(binding_id):
    return HttpResponse(json.dumps({'success': 1, 'msg': "message"}))

'''check if the binding is not existing
 after client sends the service_name,service_uid and username(SignPass)
 return 1 when binding is not existing
'''

def checkBinding(request):
    if request.method == 'POST':
        service_name = request.POST["service_name"]
        service_uid = request.POST["service_uid"]
        username = request.POST["username"]
    else:
        return HttpResponse(json.dumps({'success': 0, 'msg': "not a POST request"}))
    try:
        user = User.objects.get(username=username)
        piece = Piece.objects.get(user=user)
        service = Service.objects.get(service_name=service_name)
        binding = Binding.objects.get(service=service, service_uid=service_uid)
        if piece.id == binding.piece.id:
            return HttpResponse(json.dumps({'success': 0, 'msg': "binding is existing"}))
        else:
            return HttpResponse(json.dumps({'success': 0, 'msg': "username and service is NOT matched"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "%s not existing" % username}))
    except Piece.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "Piece not existing"}))
    except Service.DoesNotExist:
        return HttpResponse(json.dumps({'success': 0, 'msg': "service %s is not registered" % service_name}))
    except Binding.DoesNotExist:
        try:
            iPhone = IPhone.objects.get(piece=piece)
            apns = APNs(use_sandbox=True,
                cert_file="/Users/jiankaidang/Documents/MobileApplicationProgramming/CS-9033-Biometric-Password-Technology-Project/BackEnd/SignPass/sign/Certificates.pem")
            token_hex = iPhone.dev_token
            payload = Payload(alert="Connect Chase with SignPass!", sound="default", badge=1, custom={
                'username': username, 'service_name': service_name, 'service_uid': service_uid, 'requestType': 'bind'
            })
            apns.gateway_server.send_notification(token_hex, payload)
            return HttpResponse(json.dumps({'success': 1, 'msg': "binding is NOT existing"}))
        except IPhone.DoesNotExist:
            return HttpResponse(json.dumps({'success': 0, 'msg': "iphone is not registered"}))

#    except Exception as e:
#      print '%s (%s)' % (e.message, type(e))

'''check if the binding is existing by service_name,service_uid
'''

def isBound(service_name, service_uid):
    try:
        service = Service.objects.get(service_name=service_name)
        binding = Binding.objects.get(service=service, service_uid=service_uid)
        print "referenced piece is " + binding.piece.id
        return 1
    except Service.DoesNotExist:
        return 0
    except Binding.DoesNotExist:
        return 0


def verifyService(binding_id, signature):
    binding = Binding.objects.get(binding_id=binding_id)
    piece = binding.piece
    original_sign = piece.signature
    if signature == original_sign:
        return verifySuccessed(binding_id)
    elif binding.attempt_times < 5:
        binding.attempt_times += 1
        binding.save()
        return HttpResponse("please sign again")
    else:
        return HttpResponse("attempts exceed 5 times")

'''
verify if the signature is matched
'''

def verifySign(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username')
            signature = request.GET.get('signature')
            service_uid = request.GET.get('service_uid')
            service_name = request.GET.get('service_name')
            service = Service.objects.get(service_name=service_name)
            user = User.objects.get(username=username)
            piece = Piece.objects.get(user=user)
            '''requestType !=None means this is a verification for binding'''
            isMatched = random.choice([True, False])
            print isMatched
            if request.GET.get('requestType') == 'bind':
                if isMatched:#str(signature)==str(piece.signature):
                    Binding.objects.create(service=service, service_uid=service_uid, piece=piece)
                    return HttpResponse(json.dumps({'success': 1, 'msg': "signature matched"}))
                else:
                    return HttpResponse(json.dumps({'success': 0, 'msg': "signature not matched"}))
            if request.GET.get('requestType') == 'verify':
                if isMatched:#str(signature)==str(piece.signature):
                    binding = Binding.objects.get(service=service, service_uid=service_uid)
                    Verify.objects.filter(binding=binding).delete()
                    return HttpResponse(json.dumps({'success': 1, 'msg': "signature matched"}))
                else:
                #                    binding = Binding.objects.get(service=service, service_uid=service_uid)
                #                    verify = Verify.objects.filter(binding=binding)
                    #                    if verify.attempt_time == 5:
                    #                        verify.delete()
                    return HttpResponse(json.dumps({'success': 0, 'msg': "signature not matched"}))
                    #                    else:
                    #                        verify.attempt_time += 1
                    #                        return HttpResponse(json.dumps({'success': 0,
                    #                                                        'msg': "signature not matched,,you still have %d times attempt" % (
                    #                                                            6 - verify.attmept_time)}))


        except User.DoesNotExist:
            return HttpResponse(json.dumps({'success': 0, 'msg': "username not existing"}))
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))

'''
modify the signature
'''

def modifySign(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username')
            user = User.objects.get(username=username)
            piece = Piece.objects.get(user=user)
            if request.GET.get('signature') == None:
                return HttpResponse(json.dumps({'success': 0, 'msg': "no signature is caught"}))
            else:
                piece.signature = request.GET.get('signature')
                return HttpResponse(json.dumps({'success': 1, 'msg': "signature is modified"}))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'success': 0, 'msg': "username not existing"}))
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))


def index(request):
    return render_to_response("index.html", {"content": "login content"}, context_instance=RequestContext(request))


def requestFromIOS(request):
    if request.method == "GET":
        dev_token = request.GET.get("dev_token")
        udid = request.GET.get("udid")
        try:
            iPhone = IPhone.objects.get(dev_token=dev_token)
            if udid != iPhone.udid:
                iPhone.udid = udid
                iPhone.save()
        except IPhone.DoesNotExist:
            iPhone = IPhone.objects.create(dev_token=dev_token, udid=udid)
        return HttpResponse()

'''
service side sends a bind request with service_name and service_uid
'''
#@require_websocket
#def bindRequestFromBank(request,service_name,service_uid):
#  try:
#    request.websocket.wait()
#    isBound(service_name,service_uid)
#  
#    binding=Binding.objects.get(service_name=service_name,service_uid=service_uid)
#    binding.save()
#    return render_to_response("bind.html",{"service_name":service_name,"service_uid":service_uid}, context_instance=RequestContext(request))    
#  except Binding.DoesNotExist:
#    return HttpResponse(json.dumps({'success':0,'msg':"binding not existing"}))  
#  except User.DoesNotExist:
#    return HttpResponse(json.dumps({'success':0,'msg':"username not existing"}))
#  except Piece.DoesNotExist:
#    return HttpResponse(json.dumps({'success':0,'msg':"Piece not existing"}))
#  except Service.DoesNotExist:
#    return HttpResponse(json.dumps({'success':0,'msg':"service %s is not registered"%service_name}))
#  except Exception as e:
#    print '%s (%s)' % (e.message, type(e))
#    

#@accept_websocket
#def lower_case(request):
#    if not request.is_websocket():
#        message = request.GET['message']
#        return HttpResponse(message)
#    else:
#        for message in request.websocket:
#            request.websocket.send(message)

#def reg_service(request,service_name):
#  try:    

#def verify(request):
#  pass

def send_notification(request):
    apns = APNs(use_sandbox=True,
        cert_file='/Users/jiankaidang/Documents/MobileApplicationProgramming/CS-9033-Biometric-Password-Technology-Project/BackEnd/SignPass/sign/Certificates.pem')

    # Send a notification
    token_hex = IPhone.objects.all()[0].dev_token
    print token_hex
    payload = Payload(alert="Login Chase with SignPass!", sound="default", badge=1, custom={
        'userName': 'Jiankai',
        'serviceName': 'Chase'
    })
    apns.gateway_server.send_notification(token_hex, payload)
    return HttpResponse()


def isBound(service_name, service_uid):
    try:
        service = Service.objects.get(service_name=service_name)
        binding = Binding.objects.get(service=service, service_uid=service_uid)
        return binding
    except Service.DoesNotExist:
        return 0
    except Binding.DoesNotExist:
        return 0


def serviceLoginRequest(request):
#if request.method=='POST':
    service_name = request.GET['service_name']
    print service_name
    service_uid = request.GET['service_uid']
    binding = isBound(service_name, service_uid)
    if binding == 0:
        return HttpResponse(json.dumps({'success': 0, 'msg': "service_uid %d is not bound in SignPass"} % service_uid))
    else:
        try:
            #service=Service.objects.get(service_name)
            #binding=Binding.objects.get(service=service,service_uid=service_uid)
            print binding
            iPhone = IPhone.objects.get(piece=binding.piece)
            apns = APNs(use_sandbox=True,
                cert_file='/Users/jiankaidang/Documents/MobileApplicationProgramming/CS-9033-Biometric-Password-Technology-Project/BackEnd/SignPass/sign/Certificates.pem')
            # Send a notification
            token_hex = iPhone.dev_token
            payload = Payload(alert="You have a login request from %s" % service_name, sound="default", badge=1,
                custom={
                    'service_uid': service_uid, 'service_name': service_name, 'requestType': 'verify',
                    'username': binding.piece.user.username
                })
            apns.gateway_server.send_notification(token_hex, payload)
            Verify.objects.create(binding=binding, attempt_time=0)
            response = HttpResponse(request.GET['callback'] + "(" + json.dumps({'success': 1}) + ");")
        except IPhone.DoesNotExist:
            response = HttpResponse(
                request.GET['callback'] + "(" + json.dumps({'success': 0, 'msg': "iphone not existing"}) + ");")
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
        response['Content-Type'] = 'text/javascript; charset=utf8'
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'X-Requested-With'
        response['Access-Control-Allow-Methods'] = 'GET'
        return response


def loginRequestPoll(request):
#    if request.method == "POST":
    print 'def loginRequestPoll(request)'
    service_name = request.GET["service_name"]
    service_uid = request.GET["service_uid"]
    print service_name
    try:
        service = Service.objects.get(service_name=service_name)
        binding = Binding.objects.get(service=service, service_uid=service_uid)
        verify = Verify.objects.filter(binding=binding)
        if verify:
            response = HttpResponse(
                request.GET['callback'] + "(" + json.dumps({'success': 0}) + ");")
        else:
            response = HttpResponse(
                request.GET['callback'] + "(" + json.dumps({'success': 1, 'msg': "login successed"}) + ");")
    except Verify.DoesNotExist:
        response = HttpResponse(
            request.GET['callback'] + "(" + json.dumps({'success': 1, 'msg': "login successed"}) + ");")
    except Service.DoesNotExist:
        response = HttpResponse(request.GET['callback'] + "(" + json.dumps(
            {'success': 0, 'msg': "service %s is not registered" % service_name}) + ");")
    except Binding.DoesNotExist:
        response = HttpResponse(
            request.GET['callback'] + "(" + json.dumps({'success': 0, 'msg': "binding is NOT existing"}) + ");")
    response['Content-Type'] = 'text/javascript; charset=utf8'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'X-Requested-With'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response