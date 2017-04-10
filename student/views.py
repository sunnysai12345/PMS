import os

from django.core.files import File
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import StudentDB, Edit_Details,Notifications, AppliedJob
from .forms import Registerform, Loginform, EditForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random
from django.template import loader
from company.models import Register,Job_desc
# Create your views here.

#class StudentLogin(generic.TemplateView):
 #   template_name = 'student/student_login.html'

#class StudentRegistration(CreateView):
def studentregistration(request):
    status=200
    if request.method=='POST':
        form = Registerform(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            instance = form.save(commit=False)
            # if instance.c_name!=instance.c_confirm_password:
            instance.s_verification = random.randint(1, 1000)
            instance.save()
            # form.save()
            return render(request, 'student/verifymail.html')
        else:
            status = 422
    else:
        form = Registerform()
    return render(request, 'student/studentdb_form.html', {'form': form}, status=status)

    #model= StudentDB
    #fields = ['s_name', 'dob', 'emailid', 'contactno', 'address', 'profile_pic']

def studentlogin(request):
    if request.session.has_key('username') and request.session.has_key('type'):
        user=request.session['username']
        type=request.session['type']
        if(type=="student"):
            return render(request, 'student/loggedin.html', {'username': user})
        else:
            return render(request, 'company/loggedin.html', {'username': user})
    else:
        if request.method == 'POST':
            form = Loginform(data=request.POST)
            print (form.errors)
            print (form.non_field_errors)
            if form.is_valid():
                print("Validation Success")
                user = request.POST['username']
                passw = request.POST['password']
                try:
                    r = StudentDB.objects.filter(s_username__exact=user)
                    if r.filter(s_password__exact=passw):
                        if r.values()[0]['s_verified']:

                            request.session['username'] = user
                            request.session['type']= "student"
                            request.session.set_expiry(300)
                            #form = EditForm()
                            #return HttpResponseRedirect('/student/edit_details',{"username" : user})
                            return render(request,'student/loggedin.html',{'username':user})
                            #return render(request, 'student/student_editform.html', {'form': form})
                        else:
                            return render(request, 'student/verifymail.html')
                    else:
                        return render(request, 'student/invalid_login.html')
                except:
                    return render(request, 'student/invalid_login.html')
                    # instance.save()
            else:
                print("Validation Failed")
                # form = Loginform()
                return render(request, 'student/student_login.html')
        else:
            form = Loginform()
            return render(request, 'student/student_login.html', {'form': form})

#@login_required()

def view_edit(request):
    #print request.session['username']
    if request.session.has_key('username'):
        user = request.session['username']
        if request.method == 'POST':
            form = EditForm(request.POST, request.FILES)
            print (form.errors)
            print (form.non_field_errors)
            if form.is_valid():
                instance = form.save(commit=False)
                # if instance.c_name!=instance.c_confirm_password:
                instance.save()
                # instance.save()
                #print request.session['username']
                return render(request, 'student/student_editform.html', {'form': form,'username': user})
            else:
                print("Validation Failed")
                form = EditForm()
                return render(request, 'student/student_login.html', {'form': form})
        else:
            form = EditForm()
            return render(request, 'student/student_editform.html', {'form': form,'username': user})
    else:
        return HttpResponse('Invalid Access')

def auth_view(request):
    if request.method == 'GET':
        val = int(request.GET['value'])
        name = request.GET['name']
        # print(val,name)
        # print(type(val))
        r = StudentDB.objects.filter(s_username=name)[0]
        print(r)
        if r.s_verification == val:
            print("Success")
            r.s_verified = True
            r.save()
        else:
            pass
        form = EditForm()
        return render(request, 'student/verificationsuccess.html', {'form': form})
'''
def loggedin(request, user):
    if request.session.has_key('username'):
        #user=request.session['username']
        return render(request,'student/'+str(user)+'/', {'username': user})
    else:
        return HttpResponse('Invalid Access')
'''
def profile(request,username):
    if request.session.has_key('username'):
        user=request.session['username']
        s=StudentDB.objects.get(s_username=user)
        print(s.s_username)
        tmpt=Notifications.objects.filter(stdid=s)
        #form = list(tmp.values())  #show any new added job profile only i.e. if (the job id in tmp is not in notification database) and (if in notification database than boolean field is false),then append it to new list and save job_desc in n_text field of notification and set boolean variable in notification to true
        c=tmpt.count()
        ids=[]
        for i in range(0,c):
            ids.append(tmpt.values()[i]['jobid_id'])
        print(ids)
        #ids=list(tmpt.values('jobid_id'))
        form=Job_desc.objects.exclude(pk__in=ids)
        #form.extend(tmp)
        print(form)
        l=list(form.values())
        for i in range(len(l)):
            id=l[i]['id']
            idd=Job_desc.objects.get(pk=id)
            f,t = Notifications.objects.get_or_create(stdid=s,jobid=idd,n_text=str(user))
            if t:
                f.save()
        return render(request,'student/student_profile.html',{'form':form,'username':user})
    else:
        return render(request, 'student/unauthorized.html')

def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
        #auth.logout(request)
        return render(request,'student/logout_student.html')
    else:
        return render(request, 'student/unauthorized.html')

def change_password(request):
    if request.session.has_key('username'):
        user=request.session['username']
        return render(request,'student/change_password.html',{'username':user})
    else:
        return render(request, 'student/unauthorized.html')


def successfull_change(request):
    if request.session.has_key('username'):
        user=request.session['username']
        tmp=StudentDB.objects.get(s_name=user)
        try:
            old=request.POST["piCurrPass"]
            print(old)
            print(tmp.s_password)
            if tmp.s_password==old:
                tmp.s_password=request.POST["piNewPass"]
                tmp.s_confirm_password=request.POST["piNewPass"]
                tmp.save(update_fields=['s_password','s_confirm_password'])
        except:
            return render(request, 'student/unauthorized.html')
        return render(request,'student/loggedin.html',{'username':user})
    else:
        return render(request, 'student/unauthorized.html')
'''
    username= request.POST.get('username','')
    password = request.POST.get('password','')
    user=auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/student/loggedin')
    else:
        return HttpResponseRedirect('/student/invalid')


def loggedin(request):
    return render_to_response('student/loggedin.html',{'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('student/invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('student/logout.html')
'''
def notify(request,username):
    if request.session.has_key('username'):
        user = request.session['username']
        #m=Register.objects.get(c_name=user)
        sbranch = StudentDB.objects.get(s_username=user).branch
        scourse = StudentDB.objects.get(s_username=user).course
        tmp = Job_desc.objects.filter(c_branch=sbranch , c_course=scourse)
        #tmp= Job_desc.objects.all()
        form=list(tmp.values())
        print(form)
        return render(request, 'student/student_profile.html', {'form':form,'username':user})
    else:
        return render(request, 'student/unauthorized.html')

def listjobs(request):
    if request.session.has_key('username'):
        user = request.session['username']
        #m=Register.objects.get(c_name=user)
        sbranch=StudentDB.objects.get(s_username=user).branch
        scourse=StudentDB.objects.get(s_username=user).course
        print(sbranch)
        print(scourse)
        tmp= Job_desc.objects.filter(c_branch=sbranch,c_course=scourse) #need to add check that student is qualified
        form=list(tmp.values())
        print(form)
        return render(request, 'student/list_jobs.html', {'form':form,'username':user})
    else:
        return HttpResponse('Unauthorised Access')

def get_offer(request):
    if request.session.has_key('username'):
        user = request.session['username']
        sid=StudentDB.objects.get(s_username=user)
        form=AppliedJob.objects.filter(stdid= sid)# retrieve offer letters from applied jobs with jobid and attachment download link
        return render(request, 'student/offer_letter.html', {'form':form,'username':user})
    else:
        return render(request, 'student/unauthorized.html')
def update_details(request):
    if request.session.has_key('username'):
        user = request.session['username']
        s=StudentDB.objects.get(s_username=user)
        '''s_name=request.POST["s_name"]
        emailid=request.POST["emailid"]
        s.s_name=s_name
        s.emailid=emailid'''
        form = EditForm(request.POST, request.FILES, instance=s)
        form.save()
        return render(request,'student/success.html')
    else:
        return render(request, 'student/unauthorized.html')

def already_taken(request):
    print ("here");
    if request.method == "GET":
        p=request.GET.copy()
        if 'username' in p:
            name=p['username']
            if StudentDB.objects.filter(s_username__iexact=name):
                return HttpResponse("False")
            else:
                return HttpResponse("True")


def view_stud_details(request,username):
    if request.session.has_key('username'):
        user=request.session['username']
    else:
        user='Guest'
    form=StudentDB.objects.filter(s_username=username).values()
    return render(request, 'student/stud_view.html', {'form':form,'username':username})

def download(request):
    path_to_file='D:\\Github\\PMS\\media\\documents\\1.txt'
    f = open(path_to_file, 'rb')
    print(f.readlines())
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/txt')
    response['Content-Disposition'] = 'attachment;filename=1.txt'
    return response

def resumed(request,username):
    path_to_file='D:\\Github\\PMS\\media\\documents\\'+username+'.pdf'
    f = open(path_to_file, 'rb')
    print(f.readlines())
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename='+username+'.pdf'
    return response