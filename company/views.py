from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import Postform
from .forms import Loginform,EditForm,JobReqs
from .models import Register,Job_desc
from django.contrib.auth.decorators import login_required
import random
import pandas as pd
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
    if request.session.has_key('username') and request.session.has_key('type'):
        user = request.session['username']
        type = request.session['type']
        if (type == "student"):
            return render(request, 'student/loggedin.html', {'username': user})
        else:
            return render(request, 'company/loggedin.html', {'username': user})
    else:
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
                            request.session['username'] = user
                            request.session['type'] = "company"
                            request.session.set_expiry(3000)
                            #form = EditForm()
                            return render(request,'company/loggedin.html',{'username':user})
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
#@login_required()
def view_edit(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            user=request.session["username"]
            print(user)
            tmp=Register.objects.get(c_name=user)
            print(tmp.c_company_name,tmp.c_details)
            form=EditForm(request.POST,request.FILES,instance=tmp)
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
    else:
        return HttpResponse("Unauthorised Access")
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
    if request.session.has_key('username'):
        if request.method == 'POST':
            user=request.session["username"]
            m=Register.objects.get(c_name=user)
            tmp=Job_desc.objects.create(register=m)
            form=JobReqs(request.POST,instance=tmp)
            print (form.errors)
            print (form.non_field_errors)
            if form.is_valid():
                instance = form.save(commit=False)
                # if instance.c_name!=instance.c_confirm_password:
                instance.save()
                #i=Job_desc.objects.filter(c_position=instance.c_position).update(register=tmp.id)

                #instance.save()
                form=JobReqs()
                return render(request,'company/jobreqs.html',{'form':form})
            else:
                print("Validation Failed")
                #form = Loginform()
                return render(request, 'company/jobreqs.html',{'form':form})
        else:
            form = JobReqs()
            return render(request,'company/jobreqs.html',{'form':form})
    else:
        return HttpResponse("Unauthorised Access")


def profile(request,username):
    if request.session.has_key('username'):
        user=request.session['username']
        tmp=Register.objects.filter(c_name=user)
        form=tmp.values()[0]
        return render(request,'company/company_profile.html',{'username':user,'form': form})
    else:
        return HttpResponse('Unauthorised Access')

def change_password(request):
    if request.session.has_key('username'):
        user=request.session['username']
        return render(request,'company/change_password.html',{'username':user})
    else:
        return HttpResponse('Unauthorised Access')

def successfull_change(request):
    if request.session.has_key('username'):
        user=request.session['username']
        tmp=Register.objects.get(c_name=user)
        try:
            old=request.POST["piCurrPass"]
            print(old)
            print(tmp.c_password)
            if tmp.c_password==old:
                tmp.c_password=request.POST["piNewPass"]
                tmp.c_confirm_password=request.POST["piNewPass"]
                tmp.save(update_fields=['c_password','c_confirm_password'])
        except:
            return HttpResponse('Unauthorised FUCKING Access')
        return render(request,'company/loggedin.html',{'username':user})
    else:
        return HttpResponse('Unauthorised Access')
def listjobs(request):
    if request.session.has_key('username'):
        user = request.session['username']
        m=Register.objects.get(c_name=user)
        tmp= Job_desc.objects.filter(register=m)
        form=list(tmp.values())
        print(form)
        return render(request, 'company/list_jobs.html', {'form':form,'username':user})
    else:
        return HttpResponse('Unauthorised Access')

def jobdesc(request,jobid):
    #retrieve job description from database having id job id and give option to apply
    form=1#retrieved row
    return render(request, 'company/list_jobs.html', {'form':form,'jobid':jobid})