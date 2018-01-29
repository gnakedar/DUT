from django.db import models

# Create your models here.
class Platform(models.Model):

    #platform like Raspberry Pi 3,VRX200,GRX350,etc
    platform_name=models.CharField(max_length=255, help_text="Please enter platform name",default='')

class DutCategory(models.Model):
    #platform id is referenced by Platform table
    platform_id=models.ForeignKey(Platform, on_delete=models.CASCADE,default='')

    # category field having LAN,WLAN,WAN,SYSTEM etc, under platform (Raspberry Pi 3)
    category = models.CharField(max_length=250, help_text="Please enter device name")

class TestSuite(models.Model):

    # category_id is referenced by DutCategory table
    category = models.ForeignKey(DutCategory, on_delete=models.CASCADE,default='' )

    # sub_category having ShowInterfaces,AddStaticRoute,ListRoutes etc in LAN
    #sub_category = models.CharField(max_length=250, help_text="Please enter testsuite name")

    #ShowInterfaces in LAN Setup Open Station, Setup Open AP in WLAN ShowWANInterfaces in WAN
    testcasetitle = models.CharField(max_length=250,help_text="Please enter testcase title")

    #module path and space with class name
    #            module path                              class
    #--------------------------------------------------------------
    #     LAN_Verifyeth0.verifyEth0                     VerifyEth0
    #     Sys_info.systemInfo                           SystemInfo
    value = models.CharField(max_length=250,help_text="Please enter module path and space with class name ")

    #Description of testcases
    description = models.TextField(max_length=500,help_text="Please enter description of testsuite")

class TestResult(models.Model):
    platformid = models.ForeignKey(Platform, on_delete=models.CASCADE,default='' )
    categoryid = models.ForeignKey(DutCategory, on_delete=models.CASCADE,default='' )
    testsuiteid = models.ForeignKey(TestSuite,on_delete=models.CASCADE,default='')
    testcasename = models.CharField(max_length=200,unique=True,help_text="Please enter testcase name")
    status = models.CharField(max_length=50)
    executiontime = models.CharField(max_length=10)
    testcase = models.CharField(max_length=250)
    log_file_path = models.CharField(max_length=255)
