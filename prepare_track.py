#!/usr/bin/env python3
import argparse
import os
import subprocess

err = subprocess.Popen(['pip', 'install', 'ffmpeg'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

def prepare_track(input, output, ss=0, t=-14, f=3):
    print('Preparing', input + '...')
    
    # trim
    p1 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-ss', str(ss),
                           '-i', input, '-t', '60', '-f', 'wav', '-'],
                          stdout=subprocess.PIPE)
    
    # normalize
    # two-pass ebu r128 loudnorm filter
    # loudnorm pass 1
    p2 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-i', '-',
                           '-pass', '1', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                           '-f', 'wav', '-y', os.devnull],  # generate log but no other output
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    # loudnorm pass 2
    p3 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-i', '-',
                           '-pass', '2', '-af', 'loudnorm=I=' + str(t) + ':TP=-1',
                           '-f', 'wav', '-'
                           ],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    # fade
    p4 = subprocess.Popen(['ffmpeg',
                           '-loglevel', 'error',
                           '-i', '-', '-af',
                           'afade=t=in:ss=0:d=' + str(f) +
                           ',afade=t=out:st=' + str(60 - f) + ':d=' + str(f),
                           '-f', 'wav', '-y', output],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    
    trimmed = p1.communicate()[0]
    
    p2.communicate(trimmed)
    normalized = p3.communicate(trimmed)[0]
    
    return p4.communicate(normalized)[0] # return stdout in case output is '-'

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input file')
    parser.add_argument('output', type=str, help='Output file')
    parser.add_argument('-ss', type=float, default=0, help='Position to start trim at (seconds)')
    parser.add_argument('-t', type=int, default=-14, help='Target volume in LUFS (-70 to -5)')
    parser.add_argument('-f', type=float, default=3, help='Fade duration (seconds)')
    
    args = parser.parse_args()
    
    prepare_track(args.input, args.output, args.ss, args.t, args.f)
