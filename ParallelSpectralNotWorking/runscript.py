import os 
log=["alu2_log%d","apex1_log%d","apex4_log%d","C880_log%d","cm138a_log%d","cm150a_log%d","cm151a_log%d","cm162a_log%d","cps_log%d","e64_log%d","mytest_log%d","paira_log%d","pairb_log%d"]
circuitfile=["alu2.txt","apex1.txt","apex4.txt","C880.txt","cm138a.txt","cm150a.txt","cm151a.txt","cm162a.txt","cps.txt","e64.txt","mytest.txt","paira.txt","pairb.txt"]
for circuit  in range(0,len(circuitfile)):
	for multirun in range(0,20):
		logfile=log[circuit] %(multirun)
		print circuitfile[circuit]
		print logfile
		os.system("python partition.py "+circuitfile[circuit]+">"+logfile)
