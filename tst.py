# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 10:37:21 2018

@author: huang
"""

import argparse
import Main

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser()
##    parser.add_argument("-box", help="input box size", type=list)
#    parser.add_argument("-bonds", help="Largest generated bonds number", type=int)
##    parser.add_argument("-cut", help="Cutoff", type=int)
##    parser.add_argument("-gbonds", help="Generated bonds number each cycle", type=int)
#    
#    
#    args = parser.parse_args()
#    
##    print(args.box)
#    print(args.bonds)
#    parser.parse_args()
#    
#    bondTotal = args.bonds
#    

import subprocess

subprocess.call("run.sh")