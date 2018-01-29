#!/usr/bin/python

import unittest   # second test
import sys   # second test
import os
#from dummy import ConfigTestCase
#import testcases
import commonData
import importlib
import json



if (not sys.argv[2:]):
	print "Missing : List of testcases file\n"
	print "Usage:\n"
	print sys.argv[0] + " <List_of_testcases> <TestcaseResult_file\n"
	print "where List_of_testcases is a file having the testcases to be executed\n"
	print "testcaseResult_file is a file to save the testcase results\n"
	sys.exit(2)

print str(sys.argv[1])
commonData.TestcaseResult = sys.argv[2]
if (os.path.isfile(commonData.TestcaseResult)):
        os.remove(commonData.TestcaseResult)
f = open(commonData.TestcaseResult, "w+")
#f.write("Status(0-pass/1-fail) Execution_Time Testcase\n")
f.close()

def load_class(module_path, class_str):
    """
    dynamically load a class from a string
    """
    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)

#from test_sample1.test_sample1 import ConfigTestCase
#from test_sample2.test_sample1 import ConfigTestCase2
#from ssh_paramiko.ssh_paramiko import ConfigTestCase

class CreateJsonFile(unittest.TestCase):
#	def setUp(self):
#		print 'stp'
##set up code

	def runTest(self):
		writeComma = 0
		f = open(commonData.TestcaseResult + ".json", "w")
		f.write("{\"reports\":[\n");
		with open(commonData.TestcaseResult) as outfile:
			for i in outfile.readlines():
				a = i.split(' ', 2)
				print a[0]
				print a[1]
				print a[2]
				if writeComma:
					f.write(" , ")
				json.dump({'status': int(a[0]), 'executionTime': float(a[1]), 'testCase': a[2]}, f, indent=4)
				writeComma = 1
		f.write("\n]\n}");

#runs test
#		print 'stp'
#
def suite():
	"""
	Gather all the tests from this module in a test suite.
	"""
#	test_suite = unittest.TestLoader()
#	test_suite.loadTestsFromTestCase(ConfigTestCase)
#	test_suite.loadTestsFromTestCase(ConfigTestCase2)
	test_suite = unittest.TestSuite()
	#f = open('testcases.py')
	print sys.argv[1]

	testlist = open(str(sys.argv[1]))

	for line in testlist.readlines():
		a = line.split(" ")
		module = a[0]
		class1 = a[-1]
		#load_class(module,class1.rstrip("\n"))
		test_suite.addTest(unittest.makeSuite(load_class(module,class1.rstrip("\n"))))
	testlist.close()

#	test_suite.addTest(unittest.makeSuite(ConfigTestCase))
#	test_suite.addTest(unittest.makeSuite(ConfigTestCase2))
	return test_suite

mySuit=suite()
mySuit.addTest(unittest.makeSuite(CreateJsonFile))

#runner=unittest.TestLoader().loadTestsFromTestCase(ConfigTestCase)
runner=unittest.TextTestRunner(verbosity=2)

runner.run(mySuit)
