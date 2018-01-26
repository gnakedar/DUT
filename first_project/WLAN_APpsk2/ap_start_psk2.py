import paramiko
import unittest
import re
import time
import commonData
import os

class StartAPpsk2(unittest.TestCase):
        def setUp(self):
		global ssh
		self.startTime = time.time()
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(commonData.Ipaddr, commonData.Port, commonData.User, commonData.Password)
		print "\nProgressStatus@Setup WPA2-PSK AP@Started\n"

	def tearDown(self):
		t = time.time() - self.startTime
		print "%s: %.3f %d" % (self.id(), t, self.status)
		f = open(commonData.TestcaseResult, "a")
		f.write("%d\t\t\t %.3f\t\t %s\n" % (self.status, t, "Setup WPA2-PSK AP"))
	 	f.close()
                ssh.close()
                if(self.status == 0): 
                        print "ProgressStatus@Setup WPA2-PSK AP@Completed@PASS\n"
                else:
                        print "ProgressStatus@Setup WPA2-PSK AP@Completed@FAIL\n"
	

	def runTest(self):
		cwd = os.getcwd()
		run_script_path = cwd + "/WLAN_APpsk2/ap_start_psk2.sh"
		print run_script_path
		f = open(run_script_path)
                for line in f.readlines():
                        stdin,stdout,stderr=ssh.exec_command(line)
			time.sleep(2)
                        outlines=stdout.readlines()
                        resp=''.join(outlines)
			self.status = stdout.channel.recv_exit_status()
                        self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			if 'ps -w' in line:
                            if '/usr/sbin/hostapd' in resp:
                                print '\nAP is enabled'
                            else:
                                print 'AP is not enabled. Please try again'
                                break

			if 'uci get wireless.@wifi-iface[-1].ssid' in line:
			    print("SSID of AP: " + resp)

			if 'iwinfo wlan0 assoclist' in line:
			    stdin,stdout,stderr=ssh.exec_command('cat /proc/net/arp')
			    outlines=stdout.readlines()
	                    arp=''.join(outlines)
			    for str in resp.split('\n'):
				mac_addr=re.match(r'(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))',str)
				if mac_addr:
				    print "MAC address of connected station=",mac_addr.group(1)
				    for str in arp.split('\n'):
					    if mac_addr.group(1) in str.upper():
						    arp_ip=re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',str)
						    if arp_ip:
					    	        print "IP address of connected station=",arp_ip.group(1)
							print 'Ping to connected station...\n'
						        cmd = "ping -c 5 " + arp_ip.group(1)
						        stdin,stdout,stderr=ssh.exec_command(cmd)
	                        		        outlines=stdout.readlines()
						        resp=''.join(outlines)
						        print(resp)
						        self.status = stdout.channel.recv_exit_status()
						        if self.status:
						    	    print "Station %s got disconnected" % mac_addr.group(1)
			elif 'iwinfo' in line:
			    print "AP statistics:"
			    for str in resp.split('\n'):
			        if 'Channel:' in str:
			            print str
			        if 'Tx-Power:' in str:
			            print str
			        if 'Signal:' in str:
			            print str
			        if 'Bit Rate:' in str:
			            print str
			        if 'Encryption:' in str:
			            print str
			        if 'Type:' in str:
			            print str

			if 'hostapd_cli status' in line:
			    for str in resp.split('\n'):
			    	stations=re.match(r'.*num_sta\[.*=(\d{0,})', str)
			    	if stations:
			    	    print "No. of connected station(s)=",stations.group(1)
				    print "\n"
			    
		f.close()
