from django.http import HttpResponse,HttpResponseRedirect
from models import *
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext

def checkUsername(request,username):
  try:
    User.objects.get(username=username)
    return 0,HttpResponse("s% is existing"% username)
  except User.DoesNotExist:
    return 1,HttpResponse("s% is not existing"% username)

def register(request,username):  
  if checkUsername(request,username)[0]:
    return HttpResponse("s% is existing"% username)
  email=request.POST["email"] 
  signature=request.POST["signature"]   
  user=User(username=username,email=email)
  piece=Piece(user=user,signature=signature)
  user.save()
  piece.save()
  return HttpResponse("%s is created successfully"% username)
  
def bind(request,username):
  try:    
    user=User.objects.get(username=username)
    piece=Piece.objects.get(user=user)
    service=Service.objects.get(request.POST["service_id"])
    service_uid=request.POST["service_uid"]
    timestamp=datetime.datetime.now()
    binding=Binding(piece_id=piece,service_id=service,service_uid=service_uid,timestamp=timestamp)
    binding.save()
    
  except User.DoesNotExist:
    return HttpResponse("s% is not existing"% username)
  except Piece.DoesNotExist:
    return HttpResponse("piece_id is not created")
  except Service.DoesNotExist:
    return HttpResponse("service is not registered")

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
  
def verifySign(binding_id,signature):
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
  
def verifySuccessed(binding_id):
  import json
  return HttpResponse(json.dumps({'success':1,'msg':"message"}))

def checkBinding(request):
  if request.method == 'POST':
    service_id=request.POST["service_id"]
    service_uid=request.POST["service_uid"]
    import json
    return HttpResponse(json.dumps({'output_1':service_id,'output_2':service_uid}))

def index(request): 
  return render_to_response("index.html",{"content":"login content"}, context_instance=RequestContext(request))
  
#def reg_service(request,service_name):
#  try:    

#def verify(request):
#  pass
  