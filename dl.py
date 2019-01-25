#!/usr/bin/env python3

import argparse
import csv
import multiprocessing
import shutil
import os

import subprocess

err = subprocess.Popen(['pip', 'install', 'youtube-dl'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.PIPE).communicate()[1]

if len(err) != 0:
    print(err)
    exit(1)

def download(name, link, outfile):
    import subprocess
    
    print('Downloading', name, 'from', link + '...')
    process = subprocess.Popen(['youtube-dl',
                                '--extract-audio',
                                '--audio-format', 'wav',
                                '-o', outfile, link],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    
    _, err = process.communicate()
    
    if err != b'':
        import sys
        print('Error downloading', name, 'from', link, file=sys.stderr)
        print(err.decode('utf-8'), file=sys.stderr)

if __name__ == '__main__':
    
    tracks_path = os.path.join(os.path.curdir, 'tracks')
    name_index = 0
    link_index = 1
    
    if os.path.exists(tracks_path):
        shutil.rmtree(tracks_path)
    
    os.mkdir(tracks_path)
    
    with multiprocessing.Pool() as p:
        with open('klub.csv', 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            for i, row in enumerate(reader, 1):
                name = row[name_index]
                link = row[link_index]
                
                outfile = os.path.join(tracks_path, str(i) + '.wav')
                p.apply_async(download, (name, link, outfile))
        
        p.close()
        p.join()
