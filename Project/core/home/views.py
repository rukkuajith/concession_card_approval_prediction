#from http.shortcuts import render,request
from django.shortcuts import render,redirect
from home.forms import RegUser
from home.forms import Userlogin,ApplicationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate 
from home.models import Users
import pickle

# Create your views here.

def home(request):
    return render(request, 'index.html')

def register(request):

    if request.method == 'POST':
        form = RegUser(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            data=form.cleaned_data
            usr=data['username']
            pas=data['password']
            eml=data['email']
            #nmb=data['phone']
            a=User()
            a.username=usr
            a.set_password(pas)
            a.email=eml
            #a.phone=nmb
            a.save()
            

            user.save()
            form.save()
            messages.success(request,'Account is created')
            return redirect('login')
            user=authenticate(username=usr,password=pas)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'Account is created')
                    return redirect('login')
                
            
        else:
           form = Userlogin()   
    else:
        print("Please Check")
        form = RegUser()
    return render(request,'register.html',{'form':form})


# def login(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request, data=request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				login(request, user)
# 				messages.info(request, f"You are now logged in as {username}.")
# 				return redirect("application")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="login.html", context={"login_form":form})

def login(request):
    
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:

            if user.is_staff == True:
                return redirect('home')

            else:
                auth.login(request,user)
                
                return redirect('application')
                messages.info(request,f'welcome{username}')
        else:
            messages.info(request, 'invalid username and password')
            return redirect('login')
       
    else:
         return render(request,'login.html')

    

        
def application(request):
    form = ApplicationForm(request.POST)
    if request.method == 'POST':
        income = int(request.POST['income'])
        occupation = int(request.POST['occupation'])
        #if occupation =='professional':
         #   occupation=1
        #else:
         #   occupation=0
       # occupation = int(occupation)
        category = int(request.POST['category'])
        #if category =='bpl':
         #   category=1
        #else:
         #   category=0
        #category = int (category)
        result = getPredictions(income,occupation,category)
        return render(request,'result.html',{'result':result})
    else:
      return render(request,'application.html',{'form':form})



def getPredictions(income,occupation,category):
    model = pickle.load(open('model_bus','rb'))
    scaler = pickle.load(open('scaler','rb'))
    prediction = model.predict(scaler.transform([[income,occupation,category]]))
    return prediction[0]

    # if prediction == 0:
    #     return 'no'
    # elif prediction == 1:
    #     return 'yes'
    # else:
    #     return 'error'

    
# def result(request):
#     income= request.GET['income']
#     occupation = request.POST['occupation']
#     category = request.POST['category']

#     result = getPredictions(income,occupation,category)
    
#     return render(request,'result.html',{'result':result})
    






