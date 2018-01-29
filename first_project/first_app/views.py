from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import imaplib
from first_app.models import Platform,TestSuite,TestResult,DutCategory

import os
import subprocess

# Create your views here.

def index(request):
    #return HttpResponse("Welcome to Django View")
    my_dict={'insert_me':"Inside the dictionary"}
    return render(request,"index.html",context=my_dict)

def imap_login(request):
    if request.POST:
        uname = request.POST.get('username', None)
        passwd = request.POST.get('password', None)
        #print("Username and password \n", uname, passwd)
        try:
            client = imaplib.IMAP4('192.168.1.2')
            status, message = client.login(uname, passwd)
            print("status and  message ",status, message )
            user = authenticate(username=uname, password=passwd)
            if user is not None:
                login(request, user)               
                return HttpResponseRedirect("/dashboard")
            else:
                messages.error(request, "Invalide Username or password ")
                return HttpResponseRedirect("/login")

        except Exception as Ex:
            print("Exceptional is \n", Ex)
            messages.error(request, "Invalide Username or password ")
            # raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
            return HttpResponseRedirect("/login")
        finally:
            client.logout()
        
@login_required
def testcase_run(request):
    if request.POST:
        lan_showinterfaces = request.POST.get('lan_showinterfaces', None)
        wan_showwaninterfaces = request.POST.get('wan_showwaninterfaces', None)
        print("Checked box \n",lan_showinterfaces)
        print("WAN \n",wan_showwaninterfaces )
    print("Inside the lan \n\n\n\n\n")
    return render(request, "lan_category.html")



@login_required
def dashboard(request,*args, **kwargs):
    context_data={}
    platform_list=[]
    dut_category_list=[]
    testSuite_list=[]

    platform_list=Platform.objects.all()  
    dut_category_list = DutCategory.objects.all()   
    testSuite_list=TestSuite.objects.all()

    context_data['platform_list']=platform_list
    context_data['dut_category_list']=dut_category_list
    context_data['testSuite_list']=testSuite_list

    #context_data['DutCategory_list']=DutCategory_list
    for dut in dut_category_list:
        print ("DUT ID \n",dut.id)

    for plaform in platform_list:
        print("Platform data \n",plaform.platform_name)
        print("All the data \n")
    print(context_data)


    return render(request,"dashboard.html",context=context_data)
    #return render(request, "dashboard.html", platform_list,DutCategory_list )

    # if request.POST:
    #     uname = request.POST.get('username', None)
    #     passwd = request.POST.get('password', None)
    #     print("Username and password \n", uname, passwd)
    #     try:
    #         client = imaplib.IMAP4('192.168.1.2')
    #         status, message = client.login(uname, passwd)
    #         print("status and  message ",status, message )
    #     except Exception as Ex:
    #         print("Exceptional is \n", Ex)
    #         messages.error(request, "Invalide Username or password ")
    #         # raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
    #         return HttpResponseRedirect("/login")
    #     finally:
    #         client.logout()
    #     user = authenticate(username=uname, password=passwd)
    #     if user is not None:
    #         login(request, user)
    #         return render(request, "dashboard.html")
    #     else:
    #         messages.error(request, "Invalide Username or password ")
    #         return HttpResponseRedirect("/login")
    #
    #


    # p=subprocess.Popen('python2 testsuite.py  glb_2  Result_file/glb_10',shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # for line in p.stdout.readlines():
    #   print(line)
    # print(os.listdir())

    '''
    #test_result
    if request.POST:
        uname=request.POST.get('user_name',None)
        passwd = request.POST.get('passwd', None)
        print("Username and password \n",uname,passwd)
        my_dict={'uname':uname,'passwd':passwd }
        #info2 = User.objects.all()

        info=User.objects.filter()
        for i in info:
            if(i.password == passwd):
                print("YES \n")
            else:
                print("NO \n")

            print("Values \n",i,i.password)

        print("Information of auth user",info)
    '''



