#!/bin/python

import subprocess
import os


path = '/store/user/skhalil/DelphesHists/'



samples = [ 
           ['tt-4p-0-600', 'tt-4p-0-600'],
           ['tt-4p-600-1100', 'tt-4p-600-1100'], 
           ['tt-4p-1100-1700', 'tt-4p-1100-1700'],
           ['tt-4p-1700-2500', 'tt-4p-1700-2500'],
           ['tt-4p-2500-100000', 'tt-4p-2500-100000'],
           ['BB-4p-0-300', 'BB-4p-0-300'],
           ['BB-4p-300-700', 'BB-4p-300-700'],
           ['BB-4p-700-1300', 'BB-4p-700-1300'],
           ['BB-4p-1300-2100', 'BB-4p-1300-2100'],
           ['BB-4p-2100-100000', 'BB-4p-2100-100000'], 
           ['Bj-4p-0-300', 'Bj-4p-0-300'],
           ['Bj-4p-300-600', 'Bj-4p-300-600'],
           ['Bj-4p-600-1100', 'Bj-4p-600-1100'], 
           ['Bj-4p-1100-1800', 'Bj-4p-1100-1800'],
           ['Bj-4p-1800-2700', 'Bj-4p-1800-2700'],
           ['Bj-4p-2700-3700', 'Bj-4p-2700-3700'],
           ['Bj-4p-3700-100000', 'Bj-4p-3700-100000'], 
           ['tj-4p-0-500', 'tj-4p-0-500'],
           ['tj-4p-500-1000', 'tj-4p-500-1000'],
           ['tj-4p-1000-1600', 'tj-4p-1000-1600'],
           ['tj-4p-1600-2400', 'tj-4p-1600-2400'],
           ['tj-4p-2400-100000', 'tj-4p-2400-100000'],
           ['WbT_leftHanded_M1', 'Tbj_M1'],
           ['WbT_leftHanded_M1.5', 'Tbj_M1p5'], 
           ['WbT_leftHanded_M2', 'Tbj_M2'], 
           ['WbT_leftHanded_M2.5', 'Tbj_M2p5'],  
           ['WbT_leftHanded_M3', 'Tbj_M3'], 
           ['ZtT_rightHanded_M1', 'Ttj_M1'], 
           ['ZtT_rightHanded_M1.5', 'Ttj_M1p5'], 
           ['ZtT_rightHanded_M2', 'Ttj_M2'], 
           ['ZtT_rightHanded_M2.5', 'Ttj_M2p5'], 
           ['ZtT_rightHanded_M3', 'Ttj_M3'], 
           ]
               
#add them
for sample in samples :
    name =  sample[0]
    oname = sample[1]
    rootPath = path+name
    print 'xrdfsls -u '+rootPath+' | grep ".root" | wc -l'
    subprocess.call( ['xrdfsls -u '+rootPath+' | grep ".root" | wc -l'], shell=True, executable='/bin/tcsh')
    add = 'hadd '+oname+'.root   `xrdfsls -u '+rootPath+'| grep ".root"`'
    subprocess.call( [add], shell=True, executable='/bin/tcsh')
    print '------------------------------------------------------------------->'
    
