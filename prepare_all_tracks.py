#!/usr/bin/env python3
import argparse
import multiprocessing
import os
import csv
import subprocess

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', type=str, default=os.path.join(os.path.curdir, 'tracks'), help='Input folder')
    parser.add_argument('-output', type=str, default=os.path.join(os.path.curdir, 'prepared_tracks'),
                        help='Output folder')
    parser.add_argument('-t', type=int, default=-14, help='Target volume in LUFS (-70 to -5)')
    parser.add_argument('-f', type=float, default=3, help='Fade duration (seconds)')
    
    args = parser.parse_args()
    ss_index = 2

    from prepare_track import prepare_track
    
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
                
                p.apply_async(prepare_track, (infile, outfile, row[2], args.t, args.f))
        
        p.close()
        p.join()
