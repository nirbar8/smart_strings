#!/bin/python
# this script is used to run floss on a directory of files
# it will create a directory called floss_output in the same directory as the script
# and will json output for each file in the directory, keeping the same directory structure 

import os
import sys
import subprocess
from argparse import ArgumentParser 
import json

def main():
    args = ArgumentParser()
    args.add_argument('-d', '--directory', help='directory of files to run floss on')
    args.add_argument('-o', '--output', help='output directory for floss json files', default='floss_output')
    args = args.parse_args()

    if not os.path.exists(args.directory):
        print("Directory does not exist")
        sys.exit(1)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    # run floss on each file
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            file_path = os.path.join(root, file)
            output_name = root.replace('/', '_') + '_' + file + '.json'
            output_path = os.path.join(args.output, output_name)
            if os.path.exists(output_path):
                continue
            
            floss_args = ['floss', '-j', file_path, '-o', output_path]
            subprocess.run(floss_args)

            # format json files
            with open(output_path, 'r') as f:
                json_data = json.load(f)
            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=4)


if __name__ == '__main__':
    main()