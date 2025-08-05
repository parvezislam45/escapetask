from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = self.get_serializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('dashboard')
        return render(request, 'register.html', {'errors': serializer.errors})

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        serializer = self.get_serializer(data=request.POST)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'index.html', {'error': 'Invalid credentials'})
        return render(request, 'index.html', {'errors': serializer.errors})
    
def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {'user': request.user})
