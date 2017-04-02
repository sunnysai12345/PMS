from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import StudentDB, Edit_Details
from .forms import Registerform, Loginform, EditForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random
from django.template import loader
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
    if request.session.has_key('username'):
        user=request.session['username']
        return render(request, 'student/loggedin.html', {'username': user})
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
                            print ('came here')
                            print (user)
                            print (passw)
                            request.session['username'] = user
                            request.session.set_expiry(10)
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

@login_required()

def view_edit(request):
    #print request.session['username']
    if request.session.has_key('username'):
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
                return render(request, 'student/student_editform.html', {'form': form})
            else:
                print("Validation Failed")
                form = EditForm()
                return render(request, 'student/student_login.html', {'form': form})
        else:
            form = EditForm()
            return render(request, 'student/student_editform.html', {'form': form})
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
        return HttpResponse('<h1>Details for profile '+str(user)+'</h1>')
    else:
        HttpResponse('Unauthorised Access')
def logout(request):
    if request.session.has_key('username'):
        del request.session['username']
        #auth.logout(request)
        return render(request,'student/logout_student.html')
    else:
        return HttpResponse('Invalid Access')

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