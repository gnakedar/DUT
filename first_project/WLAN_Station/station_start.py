import paramiko
import unittest
import re
import time
import commonData
import os

class StartStation(unittest.TestCase):
        def setUp(self):
		global ssh
		self.startTime = time.time()
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(commonData.Ipaddr, commonData.Port, commonData.User, commonData.Password)
		print "\nProgressStatus@Setup Open Station@Started\n"

	def tearDown(self):
		t = time.time() - self.startTime
		print "%s: %.3f %d" % (self.id(), t, self.status)
		f = open(commonData.TestcaseResult, "a")
		f.write("%d\t\t\t %.3f\t\t %s\n" % (self.status, t, "Setup Open Station"))
		f.close()
                ssh.close()
                if(self.status == 0):
                        print "ProgressStatus@Setup Open Station@Completed@PASS\n"
                else:
                        print "ProgressStatus@Setup Open Station@Completed@FAIL\n"


	def runTest(self):
		cwd = os.getcwd()
		run_script_path = cwd + "/WLAN_Station/station_start_open.sh"
		print run_script_path
		f = open(run_script_path)
		for line in f.readlines():
                        print line
			stdin,stdout,stderr=ssh.exec_command(line)
			time.sleep(2)
			outlines=stdout.readlines()
			resp=''.join(outlines)
			self.status = stdout.channel.recv_exit_status()
                        self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

			if 'ps -w' in line:
			    if '/usr/sbin/wpa_supplicant' in resp:
				print 'Station is enabled\n'
			    else:
				print 'Station is not enabled'
				break
			
			elif 'wpa_cli status' in line:
			    i = 1
			    completed = False
			    while i:
			        for str in resp.split('\n'):
				    if 'bssid' in str:
				        bssid=re.match(r'bssid=(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))', str)
				    elif 'ssid' in str:
				        ssid=re.match(r'ssid=(\w{0,})',str)
                                    elif 'wpa_state' in str:
				        if 'COMPLETED' in str:
					    if completed is False:
				                print "Station connected to \"%s\" with MAC address: " % ssid.group(1),bssid.group(1)
						time.sleep(3)
					        stdin,stdout,stderr=ssh.exec_command('wpa_cli status')
					        outlines=stdout.readlines()
					        resp=''.join(outlines)
					        self.status = stdout.channel.recv_exit_status()
                        		        self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")
						completed = True
						break
					    else:
					        i = 0
						completed = False
					elif 'ASSOCIATING' in str or 'ASSOCIATED' in str:
					    stdin,stdout,stderr=ssh.exec_command('wpa_cli status')
					    outlines=stdout.readlines()
					    resp=''.join(outlines)
					    self.status = stdout.channel.recv_exit_status()
                        		    self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")
					    break
				        else:
                                            print "Could not connect to AP %s Trying to check again...\n" %str
					    i += 1
					    if i is 10:
					       print "AP is out of coverage\n"
					       i = 0
					       break
					    stdin,stdout,stderr=ssh.exec_command('wpa_cli status')
					    outlines=stdout.readlines()
					    resp=''.join(outlines)
					    self.status = stdout.channel.recv_exit_status()
                        		    self.assertEqual(stdout.channel.recv_exit_status(), 0, "Command execution failed")

				    elif 'ip_address' in str:
				        station_ip=re.match(r'ip_address=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',str)
					if station_ip:
				            print "IP address of Station: ",station_ip.group(1)
					    i = 1
					    while i:
					        found = False
				                stdin,stdout,stderr=ssh.exec_command('cat /proc/net/arp')
				                outlines=stdout.readlines()
				                arp=''.join(outlines)
				                for str in arp.split('\n'):
					            if bssid.group(1) in str:
							i = 0
						        if 'wlan' in str:
 				                            arp_ip=re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',str)
				                        if arp_ip:
							    found = True
				                            print "IP address of AP: ",arp_ip.group(1)
				                            cmd = "ping -c 5 " + arp_ip.group(1)
						            print "Ping to AP...\n\n"
				   	                    stdin,stdout,stderr=ssh.exec_command(cmd)
 				  	                    outlines=stdout.readlines()
 				 	                    resp=''.join(outlines)
							    print(resp)
				 	                    self.status = stdout.channel.recv_exit_status()
				 	                    if self.status:
				                                print "Connection lost"
							    else:
							        print '--------Station is connected to AP--------\n'
						            break
						if found is True:
						    break
						else:
						    i += 1
						    if i is 10:
	                                                print "Arp entry of AP IP is not updated. Trying with route\n"
							stdin,stdout,stderr=ssh.exec_command('route -n')
                                                	outlines=stdout.readlines()
	                                                route=''.join(outlines)
							for str in route.split('\n'):
							    if 'wlan' in str:
							        if '255.255.255.255' in str:
							    	    i = 0
							            route_ip=re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',str)
								    if route_ip:
								        found = True
								        print "IP address of AP: ",route_ip.group(1)
								        cmd = "ping -c 5 " + route_ip.group(1)
								        print "Ping to AP...\n\n"
								        stdin,stdout,stderr=ssh.exec_command(cmd)
								        outlines=stdout.readlines()
								        resp=''.join(outlines)
								        print(resp)
								        self.status = stdout.channel.recv_exit_status()
								        if self.status:
									    print "Connection lost"
								        break
				
			if 'iwinfo' in line:
			    print "Client statistics:"
			    for str in resp.split('\n'):
				    if 'Channel:' in str:
				        print str
				    elif 'Tx-Power:' in str:
				        print str
				    elif 'Signal:' in str:
				        print str
				    elif 'Bit Rate:' in str:
				        print str
				    elif 'Encryption:' in str:
				        print str
				    elif 'Type:' in str:
				        print str


		f.close()


