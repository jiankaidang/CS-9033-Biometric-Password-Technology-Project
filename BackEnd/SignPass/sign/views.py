from django.http import HttpResponse
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
#from django_websocket import require_websocket,accept_websocket

from apns import APNs, Payload

'''check if the username is existing'''
def checkUsername(request,username):
  try:
    User.objects.get(username=username)
    return HttpResponse(json.dumps({'success':0,'msg':"username existing"}))
#    return HttpResponse("Yes")
  except User.DoesNotExist:
    return HttpResponse(json.dumps({'success':1,'msg':"username not existing"}))

'''register  username + email + signature into  signpass'''
def register(request):   
  if request.method == 'GET':
    try:
      username=request.GET.get('username')
      User.objects.get(username=username)
      return HttpResponse(json.dumps({'success':0,'msg':"username existing"}))
    except User.DoesNotExist:      
      email=request.GET.get('email') 
      signature=request.GET.get('signature') 
      udid=request.GET.get('signature') 
      dev_token=request.GET.get('dev_token')
      print "udid="+udid
      try:
        user=User.objects.create(username=username,email=email)
        piece=Piece.objects.create(user=user,signature=signature)
        IPhone.objects.create(piece=piece,udid=udid,dev_token=dev_token)
        return HttpResponse(json.dumps({'success':1,'msg':"%s is created successfully"% username}))
      except Exception as e:
        print '%s (%s)' % (e.message, type(e))
#      except:
#        print sys.exc_info
      
    
'''
service side sends a bind request with service_name and service_uid
'''  
def bindRequestFromService(request,service_name,service_uid):
  try:
#    binding=Binding.objects.create(service_name=service_name,service_uid=service_uid)
#    binding.save()
    return render_to_response("bind.html",{"service_name":service_name,"service_uid":service_uid}, context_instance=RequestContext(request))    
  except Binding.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"binding not existing"}))  
  except User.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"username not existing"}))
  except Piece.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"Piece not existing"}))
  except Service.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"service %s is not registered"%service_name}))
  except Exception as e:
    print '%s (%s)' % (e.message, type(e))

def bindRequestPoll(request):
  if request.method=="POST":
      service_name=request.POST["service_name"]
      service_uid=request.POST["service_uid"]
  try:
    service=Service.objects.get(service_name=service_name)
    if Binding.objects.get(service=service,service_uid=service_uid):
      return HttpResponse(json.dumps({'success':1,'msg':"binding successed"}))
  except Service.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"service %s is not registered"%service_name}))
  except Binding.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"binding is NOT existing"}))

def checkServicename(request,service_name):
  try:
    User.objects.get(service_name=service_name)
    return HttpResponse("s% is existing"% service_name)
  except User.DoesNotExist:
    return HttpResponse("s% is not existing"% service_name)
  
def find_iOS(binding_id):
  pass

def createVerify(binding):
  Verify.objects.create(binding=binding)
  
def verifySuccessed(binding_id):
  return HttpResponse(json.dumps({'success':1,'msg':"message"}))

'''check if the binding is not existing
 after client sends the service_name,service_uid and username(SignPass)
 return 1 when binding is not existing
'''
def checkBinding(request):
  if request.method == 'POST':
    service_name=request.POST["service_name"]
    service_uid=request.POST["service_uid"]
    username=request.POST["username"]
  else:
    return HttpResponse(json.dumps({'success':0,'msg':"not a POST request"}))
  try:
    user=User.objects.get(username=username)
    piece=Piece.objects.get(user=user)
    service=Service.objects.get(service_name=service_name)
    binding=Binding.objects.get(service=service,service_uid=service_uid)
    if piece.id==binding.piece.id:
      return HttpResponse(json.dumps({'success':0,'msg':"binding is existing"}))
    else:
      return HttpResponse(json.dumps({'success':0,'msg':"username and service is NOT matched"}))
  except User.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"%s not existing"%username}))
  except Piece.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"Piece not existing"}))
  except Service.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"service %s is not registered"%service_name}))
  except Binding.DoesNotExist:
    try:
      iPhone=IPhone.objects.get(piece=piece)
      apns = APNs(use_sandbox=True, cert_file='/Users/jiankaidang/Documents/MobileApplicationProgramming/CS-9033-Biometric-Password-Technology-Project/BackEnd/SignPass/sign/Certificates.pem')
      token_hex = iPhone.dev_token
      payload = Payload(alert="Login Chase with SignPass!", sound="default", badge=1, custom={
          'userName':username ,
          'serviceName': service_name
      })
      apns.gateway_server.send_notification(token_hex, payload)
      return HttpResponse(json.dumps({'success':1,'msg':"binding is NOT existing"}))
    except IPhone.DoesNotExist:  
      return HttpResponse(json.dumps({'success':0,'msg':"iphone is not registered"}))
#    except Exception as e:
#      print '%s (%s)' % (e.message, type(e))
  
'''check if the binding is existing by service_name,service_uid
'''
def isBound(service_name,service_uid):
  try:
    service=Service.objects.get(service_name=service_name)
    binding=Binding.objects.get(service=service,service_uid=service_uid)
    print "referenced piece is "+binding.piece.id
    return 1
  except Service.DoesNotExist:
    return 0
  except Binding.DoesNotExist:
    return 0
  
def verifyService(binding_id,signature):
  binding=Binding.objects.get(binding_id=binding_id)
  piece=binding.piece
  original_sign=piece.signature  
  if signature==original_sign:
    return verifySuccessed(binding_id)
  elif binding.attempt_times<5:
    binding.attempt_times+=1
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
      username=request.GET.get('username')  
      user=User.objects.get(username=username)     
      piece=Piece.objects.get(user=user)
      signature=request.GET.get('signature')
      if str(signature)==str(piece.signature): 
        return HttpResponse(json.dumps({'success':1,'msg':"signature matched"}))
      else:
        return HttpResponse(json.dumps({'success':0,'msg':"signature not matched"}))
    except User.DoesNotExist:
      return HttpResponse(json.dumps({'success':0,'msg':"username not existing"}))
    except Exception as e:
      print '%s (%s)' % (e.message, type(e))

'''
modify the signature
'''
def modifySign(request):
  if request.method == 'GET':
    try:
      username=request.GET.get('username')  
      user=User.objects.get(username=username)     
      piece=Piece.objects.get(user=user)
      if request.GET.get('signature')==None:
        return HttpResponse(json.dumps({'success':0,'msg':"no signature is caught"}))
      else: 
        piece.signature=request.GET.get('signature')
        return HttpResponse(json.dumps({'success':1,'msg':"signature is modified"}))
    except User.DoesNotExist:
      return HttpResponse(json.dumps({'success':0,'msg':"username not existing"}))
    except Exception as e:
      print '%s (%s)' % (e.message, type(e))

def index(request): 
  return render_to_response("index.html",{"content":"login content"}, context_instance=RequestContext(request))


def requestFromIOS(request):
  if request.method=="GET":
    dev_token = request.GET.get("dev_token")
    udid= request.GET.get("udid")
    try:
        iPhone = IPhone.objects.get(dev_token=dev_token)
        if udid!=iPhone.udid:
          iPhone.udid=udid
          iPhone.save()
    except iPhone.DoesNotExist:
        iPhone = IPhone.objects.create(dev_token=dev_token,udid=udid)
    return HttpResponse()


def serviceLoginRequest(request,service_name,service_uid,username):
  try:
    print service_name
    service_name=service_name
    service_uid=service_uid
    service=Service.objects.get(service_name)
    binding=Binding.objects.get(service=service,service_uid=service_uid)
    iPhone=IPhone.objects.get(binding.piece)
    print "serviceLoginRequest"
    apns = APNs(use_sandbox=True, cert_file='/Users/jiankaidang/Documents/MobileApplicationProgramming/CS-9033-Biometric-Password-Technology-Project/BackEnd/SignPass/sign/Certificates.pem')

    # Send a notification
    token_hex = iPhone.dev_token
    print token_hex
    payload = Payload(alert="Login Chase with SignPass!", sound="default", badge=1, custom={
        'userName':username ,
        'serviceName': service_name
    })
    apns.gateway_server.send_notification(token_hex, payload)
  except Binding.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"binding not existing"}))  
  except IPhone.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"iphone not existing"}))
  except Service.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"service %s is not registered"%service_name}))
  except Exception as e:
    print '%s (%s)' % (e.message, type(e))
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
    apns = APNs(use_sandbox=True, cert_file='/Users/jiankaidang/Documents/MobileApplicationProgramming/CS-9033-Biometric-Password-Technology-Project/BackEnd/SignPass/sign/Certificates.pem')

    # Send a notification
    token_hex = IPhone.objects.all()[0].dev_token
    print token_hex
    payload = Payload(alert="Login Chase with SignPass!", sound="default", badge=1, custom={
        'userName': 'Jiankai',
        'serviceName': 'Chase'
    })
    apns.gateway_server.send_notification(token_hex, payload)
    return HttpResponse()