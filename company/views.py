from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Postform
from .forms import Loginform,EditForm,JobReqs
from .models import Register
from django.contrib.auth.decorators import login_required
import random
# Create your views here.
def post_list(request):
    status = 200
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Postform(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            instance=form.save(commit=False)
            #if instance.c_name!=instance.c_confirm_password:
            instance.c_verification = random.randint(1,1000)
            instance.save()
            #form.save()
            return render(request, 'company/verifymail.html')
        else:
            status = 422
    else:
        form=Postform()
    return render(request, 'company/tempform.html', {'form':form},status=status)
def view_home(request):
    if request.method == 'POST':
        form=Loginform(data=request.POST)
        print (form.errors)
        print (form.non_field_errors)
        if form.is_valid():
            print("Validation Success")
            user=request.POST['username']
            passw=request.POST['password']
            try:
                r=Register.objects.filter(c_name__exact=user)
                if r.filter(c_password__exact=passw):
                    if r.values()[0]['c_verified'] :
                        form = EditForm()
                        return render(request,'company/companyform.html',{'form':form})
                    else:
                        return render(request,'company/verifymail.html')
                else:
                    return render(request, 'company/login_failure.html')
            except:
                return render(request,'company/login_failure.html')
            #instance.save()
        else:
            print("Validation Failed")
            #form = Loginform()
            return render(request, 'company/login.html')
    else:
        form=Loginform()
        return render(request,'company/login.html',{'form':form})
@login_required()
def view_edit(request):
    if request.method == 'POST':
        form=EditForm(request.POST,request.FILES)
        print (form.errors)
        print (form.non_field_errors)
        if form.is_valid():
            instance = form.save(commit=False)
            # if instance.c_name!=instance.c_confirm_password:
            instance.save()
            #instance.save()
            return render(request,'company/companyform.html',{'form':form})
        else:
            print("Validation Failed")
            #form = Loginform()
            return render(request, 'company/companyform.html',{'form':form})
    else:
        form = EditForm()
        return render(request,'company/companyform.html',{'form':form})
def verify(request):
    if request.method == 'GET':
        val=int(request.GET['value'])
        name=request.GET['name']
        #print(val,name)
        #print(type(val))
        r=Register.objects.filter(c_name=name)[0]
        print(r)
        if r.c_verification == val:
            print("Success")
            r.c_verified=True
            r.save()
        else:
            pass
        form = EditForm()
        return render(request, 'company/verificationsuccess.html', {'form': form})
def Jobreqs(request):
    form = JobReqs()
    return render(request, 'company/jobreqs.html', {'form': form})
