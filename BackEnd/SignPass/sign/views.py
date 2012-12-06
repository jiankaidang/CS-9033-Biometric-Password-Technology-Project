from django.http import HttpResponse,HttpResponseRedirect
from models import *
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
import json,sys

def checkUsername(request,username):
  try:
    User.objects.get(username=username)
    return HttpResponse(json.dumps({'success':0,'msg':"username existing"}))
#    return HttpResponse("Yes")
  except User.DoesNotExist:
    return HttpResponse(json.dumps({'success':1,'msg':"username not existing"}))

def register(request):   
  if request.method == 'GET':
    try:
      username=request.GET.get('username')
      print username
      User.objects.get(username=username)
      return HttpResponse(json.dumps({'success':0,'msg':"username existing"}))
    except User.DoesNotExist:
      email=request.GET.get('email') 
      print email
      signature=request.GET.get('signature')  
      print signature 
      try:
        user=User.objects.create(username=username,email=email)
        Piece.objects.create(user=user,signature=signature)
      except Exception as e:
        print '%s (%s)' % (e.message, type(e))
#      except:
#        print sys.exc_info
      return HttpResponse(json.dumps({'success':1,'msg':"%s is created successfully"% username}))
  
def bindRequestFromBank(request,service_name,service_uid):
  try:
#    service=Service.objects.get(request.POST["service_id"])
#    service_uid=request.POST["service_uid"]
    binding=Binding(service_name=service_name,service_uid=service_uid)
    binding.save()
    return render_to_response("bind.html",{"service_name":service_name,"service_uid":service_uid}, context_instance=RequestContext(request))    
  except User.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"username not existing"}))
  except Piece.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"Piece not existing"}))
  except Service.DoesNotExist:
    return HttpResponse(json.dumps({'success':0,'msg':"service %s is not registered"%service_name}))
  
def bind(request):
  if request.method=="POST":
    service_name=request.POST["service_name"]
    service_uid=request.POST["service_uid"]
    username=request.POST["username"]
    timestamp=datetime.datetime.now()
    user=User.objects.get(username=username)
    piece=Piece.objects.get(user=user)
    service=Service.objects.get(service_name=service_name)
    Binding.objects.create(piece=piece,service=service,service_uid=service_uid,binding_time=timestamp)

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

def checkBinding(request):
  if request.method == 'POST':
    service_id=request.POST["service_id"]
    service_uid=request.POST["service_uid"]
    return HttpResponse(json.dumps({'output_1':service_id,'output_2':service_uid}))
  
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


  
#def reg_service(request,service_name):
#  try:    

#def verify(request):
#  pass
  
