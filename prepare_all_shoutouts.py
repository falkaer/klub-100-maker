#!/usr/bin/env python3
import argparse
import csv
import multiprocessing
import os
import subprocess

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', type=str, default=os.path.join(os.path.curdir, 'shoutouts'), help='Input folder')
    parser.add_argument('-output', type=str, default=os.path.join(os.path.curdir, 'prepared_shoutouts'),
                        help='Output folder')
    parser.add_argument('-t', type=int, default=-14, help='Target volume in LUFS (-70 to -5)')
    
    args = parser.parse_args()
    
    from prepare_shoutout import prepare_shoutout
    
    if not os.path.exists(args.input):
        exit(1)
    
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    
    with multiprocessing.Pool() as p:
        with open('klub.csv', 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            for i, row in enumerate(reader, 1):
                
                infile = os.path.join(args.input, str(i) + '.wav')
                outfile = os.path.join(args.output, str(i) + '.wav')
                
                if not os.path.exists(infile):
                    continue
                
                p.apply_async(prepare_shoutout, (infile, outfile, args.t))
        
        p.close()
        p.join()
