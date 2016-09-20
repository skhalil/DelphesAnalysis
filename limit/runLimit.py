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

    print "combine -n _Expected_"+sig+"_M"+mass+"  -M Asymptotic --run=expected limit/datacards_shape/"+sig+"_M"+mass+"_card.txt" 
   
    os.system("combine -n _Expected_"+sig+"_M"+mass+" -M Asymptotic --run=expected limit/datacards_shape/"+sig+"_M"+mass+"_card.txt")

os.system("hadd -f higgsCombine_Expected_"+sig+".Asymptotic.root higgsCombine_Expected_"+sig+"_M*.Asymptotic.mH*.root")
#os.system("rm -rf higgsCombine_Expected_"+sig+"_M*.Asymptotic.mH*.root")
