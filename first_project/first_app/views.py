from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
import subprocess

# Create your views here.

def index(request):
    #return HttpResponse("Welcome to Django View")
    my_dict={'insert_me':"Inside the dictionary"}
    return render(request,"index.html",context=my_dict)

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

    #p=subprocess.Popen('python2 testsuite.py  glb_2  Result_file/glb_10',shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #for line in p.stdout.readlines():
     #   print(line)
    #print(os.listdir())
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

    return render(request,"dashboard.html")


# @login_required
# def lan(request):
#     print("Inside the lan \n\n\n\n\n")
#     return render(request, "lan_category.html")
#
#
# @login_required
# def wan(request):
#     print("Inside the lan \n\n\n\n\n")
#     return render(request, "wan_category.html")
#
# @login_required
# def wlan(request):
#     print("Inside the lan \n\n\n\n\n")
#     return render(request, "wlan_category.html")
#
# @login_required
# def system(request):
#     print("Inside the lan \n\n\n\n\n")
#     return render(request, "system_category.html")
#
