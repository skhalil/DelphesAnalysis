#!/usr/bin/env python
import os
import re
import sys
import time
import commands

from os.path import join, getsize

masspoints = [1000, 1500, 2000, 2500, 3000]
sig = "Tbj"

for m in masspoints:
    print '-----mass = ',m ,' ----------'
    mass = str(m)
    os.system("combine -n "+sig+" -S 0 -m "+mass+" --rMin=0.001 --rMax=0.2 -M Asymptotic datacards/"+sig+"_M"+mass+"card.txt")    

os.system("hadd -f higgsCombine"+sig+".Asymptotic.root higgsCombine"+sig+".Asymptotic.mH*.root")
os.system("rm -rf higgsCombine"+sig+".Asymptotic.mH*.root")
