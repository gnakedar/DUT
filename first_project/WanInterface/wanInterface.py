import unittest
import subprocess
import time
import paramiko		# SSH Support
import commonData
import os
import re


class WanInterface(unittest.TestCase):
	def setUp(self):
		self.startTime = time.time()
		global ssh
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(commonData.Ipaddr, commonData.Port, commonData.User, commonData.Password)
                print "\nProgressStatus@ShowWANInterfaces@Started\n"

	def tearDown(self):
		t = time.time() - self.startTime
		print "%s: %.3f %d" % (self.id(), t, self.status)
		f = open(commonData.TestcaseResult, "a")
		f.write("%d\t\t\t %.3f\t\t %s\n" % (self.status, t, "ShowWANInterfaces"))
		f.close()
		ssh.close()
                if(self.status == 0):
                        print "ProgressStatus@ShowWANInterfaces@Completed@PASS\n"
                else:
                        print "ProgressStatus@ShowWANInterfaces@Completed@FAIL\n"


	def runTest(self):
		cwd = os.getcwd()
		run_script_path = cwd + "/WanInterface/wanInterface.sh"
		fp = open(run_script_path, "r")
		wan_interface = ''
		default_gateway = ''

		for cmd in fp.readlines():
			cmd = cmd.strip('\n')	# Removing the newline
			if 'uci get network.wan.ifname' in cmd:
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				wan_interface = resp.strip('\n')	# Removing the newline
				print "WAN Interface: %s" % wan_interface
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif 'route -n' in cmd:
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				print resp
				for line in resp.split('\n'):
					def_gate = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*(255.255.255.255).*%s' % wan_interface, line)
					if def_gate:
						default_gateway = def_gate.group(1)
						print "default_gateway: %s" % default_gateway
						break
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif 'ping -c 3' in cmd:
				cmd = cmd + ' ' +  default_gateway
				print cmd
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				print resp
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

		fp.close()

