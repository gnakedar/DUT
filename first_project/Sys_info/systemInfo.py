import unittest
import subprocess
import time
import paramiko		# SSH Support
import os
import commonData

cmd = ""

class SystemInfo(unittest.TestCase):
	def setUp(self):
		self.startTime = time.time()
		global ssh
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#		ssh.connect(HOST, port, user, password)
		ssh.connect(commonData.Ipaddr, commonData.Port, commonData.User, commonData.Password)
		print "\nProgressStatus@System Info@Started\n"

	def tearDown(self):
		t = time.time() - self.startTime
                print "%s: %.3f %d" % (self.id(), t, self.status)
                f = open(commonData.TestcaseResult, "a")
                f.write("%d\t\t\t %.3f\t\t %s\n" % (self.status, t, "System Info"))
                f.close()
		ssh.close()
                if(self.status == 0):
                        print "ProgressStatus@System Info@Completed@PASS\n"
                else:
                        print "ProgressStatus@System Info@Completed@FAIL\n"


	def runTest(self):
		cwd = os.getcwd()
		run_script_path = cwd + "/Sys_info/systemInfo.sh"
		fp = open(run_script_path, "r")
		for cmd in fp.readlines():
			print cmd
			stdin, stdout, stderr = ssh.exec_command(cmd)
			ping = stdout.readlines()
			resp=''.join(ping)
			self.status = stdout.channel.recv_exit_status()
	                self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")
			print(resp)
		fp.close()

