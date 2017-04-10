from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import Postform
from .forms import Loginform,EditForm,JobReqs
from .models import Register,Job_desc
from django.contrib.auth.decorators import login_required
import random
from student.models import Notifications,AppliedJob,StudentDB
from django.core.mail import send_mail
# Create your views here.
def post_list(request):
    status = 200
    print('hello')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Postform(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            instance=form.save(commit=False)
            #print(instance.c_password)
            #print(instance.c_confirm_password)
            instance.c_verification = random.randint(1,1000)
            instance.save()

            #form=Postform()
            #return render(request, 'company/tempform.html', {'form': form}, status=status)
            #form.save()
            '''send_mail(
                'Verification Mail',
                'Please verify the mail id by clicking on the below link http:localhost:8000/company/verify/'+str(instance.c_verification),
                'sunnysai12345@iitkgp.ac.in',
                ['sunnysai12345@gmail.com'],
            )'''
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
            #print (form.errors)
            #print (form.non_field_errors)
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
        user = request.session["username"]
        if request.method == 'POST':
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
                return render(request,'company/companyform.html',{'form':form, 'username':user})
            else:
                print("Validation Failed")
                #form = Loginform()
                return render(request, 'company/companyform.html',{'form':form,'username':user})
        else:
            form = EditForm()
            return render(request,'company/companyform.html',{'form':form,'username':user})
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
    disable=""
    if request.session.has_key('username'):
        user = request.session['username']
        request.session['jobid'] = jobid
    else:
        user="Guest"
        disable="disabled"

    tmp=Job_desc.objects.filter(pk=jobid)
    t=Job_desc.objects.get(pk=jobid)
    form=list(tmp.values())#retrieved row
    name = Register.objects.get(pk=t.register_id).c_name
    return render(request, 'company/apply_job.html', {'form':form,'company':name,'jobid':jobid,'username':user,'disabled':disable})

def jobapplied(request):
    #store student Id to applied, display a student profile page
    if request.session.has_key('jobid') and request.session.has_key('username'):
        jobid=request.session['jobid']
        user=request.session['username']
    else:
        jobid=1
        user="Guest"
    j=Job_desc.objects.get(pk=jobid)
    if user in j.list_of_student.split(","):
        return HttpResponse("Already applied... why are you fucking not serious..you asshole")
    else:
        s=StudentDB.objects.get(s_username=user)
        a=AppliedJob(stdid=s,jobid=j)
        a.applied=True
        a.save()
        if(len(j.list_of_student)==0):
            j.list_of_student=user
        else:
            j.list_of_student=j.list_of_student+","+user
        j.save()
        return render(request, 'student/applied_msg.html')

def view_student_list(request,jobid):
    n=Job_desc.objects.get(pk=jobid)
    stdnames=n.list_of_student.split(",")
    form=stdnames
    request.session['offerid']=jobid
    return render(request, 'company/student_list.html',{'form':form})

def already_taken(request):
    print ("here");
    if request.method == "GET":
        p=request.GET.copy()
        if 'username' in p:
            name=p['username']
            if Register.objects.filter(c_name__iexact=name):
                return HttpResponse("False")
            else:
                return HttpResponse("True")

def offered(request,userid):
    if request.session.has_key('offerid'):
        jobid=request.session['offerid']
        sid=StudentDB.objects.get(s_username=userid)
        j=Job_desc.objects.get(pk=jobid)
        a=AppliedJob.objects.get(stdid=sid,jobid=j)
        a.got_offer="Yes"
        a.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)