from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'sign-up-page.html')
# # def login(request):
# #     return render(request,'login.html')

