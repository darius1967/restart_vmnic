#!/bin/python
import time
import subprocess
import sys
f1=open("/opt/F80",'r') #virtual machines name and ip to be checked like VM;IP
A1=f1.readlines()
d={}
f1.close()
s=30
for i in A1:
        d[i.strip('\n').split(';')[0]]=[i.strip('\n').split(';')[1],0]
while(True):
        l=time.localtime(time.time())
        timp=str(l.tm_mon)+"-"+str(l.tm_mday)+"-"+str(l.tm_year)+"-"+str(l.tm_hour)+"-"+str(l.tm_min)
        if l.tm_sec==s:
                for i in d.keys():
                        c1=subprocess.Popen("net-stats -l |grep -i "+i+"|grep vSwitch", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
                        if len(c1.decode("utf-8"))>0:
                                f=subprocess.Popen("vim-cmd vmsvc/getallvms|grep -i "+i,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
                                g=subprocess.Popen("vim-cmd vmsvc/power.getstate "+str(f.decode("utf-8").split()[0]),shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
                                if "Powered off" not in g.decode("utf-8"):
                                        c2=subprocess.Popen("ping -c2 -W 1 "+d[i][0], shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
                                        if "100%" in str(c2):
                                                d[i][1]=d[i][1]+1
                                                if d[i][1]>3:
                                                        c3=subprocess.Popen("esxcfg-vswitch -l|grep "+c1.split()[3].decode("utf-8"),shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
                                                        v = [ j for j in c3.decode("utf-8").strip("\n").split()[len(c3.decode("utf-8").strip("\n").split())-1].split(',') ]
                                                        for v1 in v:
                                                                c4=subprocess.call("esxcli network nic down -n "+v1+" && esxcli network nic up -n "+v1, shell=True)
                                                                c5=subprocess.Popen("logger f80.py "+i+" "+v1+" "+timp,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
                                                        d[i][1]=0
                                        else:
                                                c5=subprocess.Popen("logger "+i+" "+timp,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
                                else:
                                        d[i][1]=0
                        else:
                                if d[i][1]>0:
                                        d[i][1]=0
