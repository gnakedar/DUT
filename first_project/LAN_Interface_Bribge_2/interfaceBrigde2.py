import unittest
import subprocess
import time
import paramiko		# SSH Support
import commonData
import os
import re


class InterfaceBridge2(unittest.TestCase):
	def setUp(self):
		self.startTime = time.time()
		global ssh
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(commonData.Ipaddr, commonData.Port, commonData.User, commonData.Password)
		print "\nProgressStatus@Change Subnet@Started\n"

	def tearDown(self):
		t = time.time() - self.startTime
		print "%s: %.3f %d" % (self.id(), t, self.status)
		f = open(commonData.TestcaseResult, "a")
		f.write("%d\t\t\t %.3f\t\t %s\n" % (self.status, t, "Change Subnet"))
		f.close()
		ssh.close()
                if(self.status == 0): 
                        print "ProgressStatus@Change Subnet@Completed@PASS\n"
                else:
                        print "ProgressStatus@Change Subnet@Completed@FAIL\n"


	def runTest(self):
		cwd = os.getcwd()
		run_script_path = cwd + "/LAN_Interface_Bribge_2/interfaceBrigde2.sh"
		fp = open(run_script_path, "r")
		bridge_ip = ''
		bridge_ip_new = ''
		device_ip = ''
		flag = True
		ping_flag = True

		for cmd in fp.readlines():
			cmd = cmd.strip('\n')	# Removing the newline
			if 'uci get network.lan.ipaddr' in cmd:
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				if flag:
					bridge_ip = resp.strip('\n')	# Removing the newline
					print 'brigde_ip: %s' % bridge_ip
					flag = False
				else:
					bridge_ip_new = resp.strip('\n')	# Removing the newline
					print 'brigde_ip_new: %s' % bridge_ip_new
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif 'cat /var/dhcp.leases' in cmd:
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				print resp
				for line in resp.split('\n'):
					def_gate = re.match(r'.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*', line)
					if def_gate:
						device_ip = def_gate.group(1)
						print "device_ip: %s" % device_ip
						break
					else:
						pass
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif 'ping -c 3' in cmd:
				if ping_flag:
					if device_ip:
						cmd = cmd + ' ' +  device_ip
					else:
						cmd = cmd + ' ' +  bridge_ip
					stdin, stdout, stderr = ssh.exec_command(cmd)
					ping = stdout.readlines()
					resp=''.join(ping)
					print resp
					ping_flag = False
					self.status = stdout.channel.recv_exit_status()
					self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")
				else:
					if device_ip:
						cmd = cmd + ' ' +  device_ip
					else:
						cmd = cmd + ' ' +  bridge_ip
					stdin, stdout, stderr = ssh.exec_command(cmd)
					ping = stdout.readlines()
					resp=''.join(ping)
					print resp
					self.status = stdout.channel.recv_exit_status()
					self.assertNotEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")


			elif 'uci set network.lan.ipaddr' in cmd:
				new_ip = re.match(r'(\d{1,3}\.\d{1,3}\.)(\d{1,3})(\.\d{1,3})', bridge_ip)
				str1, str2, str3 = new_ip.group(1), new_ip.group(2), new_ip.group(3)
				str2 = int(str2) +1
				str2 = str(str2)
				new_ip = str1 + str2 + str3
				cmd = cmd + '=' + new_ip
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif '/etc/init.d/network reload' in cmd:
				stdin, stdout, stderr = ssh.exec_command(cmd)
				ping = stdout.readlines()
				resp=''.join(ping)
				self.status = stdout.channel.recv_exit_status()
				self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			elif 'reset_all' in cmd:
			#Cleaning option as the bridge ip has been modified in test case
				cmd = 'uci set network.lan.ipaddr'
				cmd = cmd + '=' + bridge_ip
				stdin, stdout, stderr = ssh.exec_command(cmd)
				cmd = 'uci commit'
				stdin, stdout, stderr = ssh.exec_command(cmd)
				cmd = '/etc/init.d/network reload'
				stdin, stdout, stderr = ssh.exec_command(cmd)

		fp.close()
