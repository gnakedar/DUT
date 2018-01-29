import unittest
import subprocess
import time
import paramiko		# SSH Support
import commonData
import os
import re


class InterfaceBridge(unittest.TestCase):
	def setUp(self):
		self.startTime = time.time()
		global ssh
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(commonData.Ipaddr, commonData.Port, commonData.User, commonData.Password)
		print "\nProgressStatus@List LAN Interfaces@Started\n"

	def tearDown(self):
		t = time.time() - self.startTime
		print "%s: %.3f %d" % (self.id(), t, self.status)
		f = open(commonData.TestcaseResult, "a")
		f.write("%d\t\t\t %.3f\t\t %s\n" % (self.status, t, "List LAN Interfaces"))
		f.close()
		ssh.close()
                if(self.status == 0):
                        print "ProgressStatus@List LAN Interfaces@Completed@PASS\n"
                else:
                        print "ProgressStatus@List LAN Interfaces@Completed@FAIL\n"


	def runTest(self):
		cwd = os.getcwd()
		run_script_path = cwd + "/LAN_Interface_Bribge_1/interfaceBrigde.sh"
		fp = open(run_script_path, "r")
		lan_interface = ''
		lan_bridge = ''
		brigde_ip = ''

		for cmd in fp.readlines():
			cmd = cmd.strip('\n')	# Removing the newline
			if 'uci get network.lan.ifname' in cmd:
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				lan_interface = resp.strip('\n')	# Removing the newline
				print "LAN Interface: %s" % lan_interface
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif 'brctl show' in cmd:
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				print resp
				for line in resp.split('\n'):
					def_gate = re.match(r'^(\w+\W+\w+).*%s' % lan_interface, line)
					if def_gate:
						lan_bridge = def_gate.group(1)
						print "lan_bridge: %s" % lan_bridge
						break
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif 'ifconfig' in cmd:
				cmd = cmd + ' ' + lan_bridge
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				print resp
				for line in resp.split('\n'):
					mat = re.match(r'.*inet addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*', line)
					if mat:
						brigde_ip = mat.group(1)
						print 'brigde_ip: %s' % brigde_ip
						break

			elif 'ping -c 3' in cmd:
				cmd = cmd + ' ' +  brigde_ip
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				print resp
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

		fp.close()

