from django.contrib.auth import authenticate, login 
from django.http import JsonResponse
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import auth
from users.models import ApplicationUser

# Register View 

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @csrf_exempt
    def post(self,request):
        full_name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        confirmPassword = request.data.get("confirmPassword")
        phone = request.data.get("phone")
        nid = request.data.get("nid") 
        
        
        if not password:
            return Response({"status":"error", "message":"User already exists"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        
        if ApplicationUser.objects.filter(nid=nid).exists():
            return Response({'status':'error','message':'Username already exists'}, status=status.HTTP_208_ALREADY_REPORTED)
        
        user = ApplicationUser.objects.create_user(username= nid, password=password, first_name = full_name, phone_number = phone,nid=nid,email=email,user_type='Patient')
        user.save()
        return Response({'status':'success', 'message':'User created successfully'}, status=status.HTTP_201_CREATED)
    
        
# Login View 
@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request):
        if request.user.is_authenticated:
            return Response({
                "user_type":request.user.user_type,
            })        
        
        return Response({"details":"Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self,request):
        email = request.data.get('identifier')
        password = request.data.get("password")
        
        user = authenticate(request, username = email, password= password)
        
        if user is not None:
            login(request, user)
            return Response({'status':"success","message":"Logges in successfully","user_type":user.user_type})
        return Response({"status":"error", 'message':"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)


@ensure_csrf_cookie   
def csrf(request):
    return JsonResponse({"Message": "CSRF cookie set"}) 

from django.contrib.auth.decorators import login_required

@login_required 
def current_user(request):
    return JsonResponse({"username":request.user.username})


def logout(request):
    auth.logout(request)
    return JsonResponse({"status":"success", "message":"Logged out successfully"})

