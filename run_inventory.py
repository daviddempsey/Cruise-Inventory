#!/usr/bin/env python
import os
import sys
from config import *
from scripts import *
import logging

# run_inventory.py
# Created by David Dempsey
# email: ddempsey@ucsd.edu

args = sys.argv

def run_inventory(cruise):
    """
    Runs inventory on a given cruise.

    cruise: A given cruise
    """
    logging.info('Running inventory on ' + cruise + '\n')
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              'Running inventory on ' + cruise + '\n')
    ship_abbreviation = get_ship_abbreviation(cruise.upper())
    datadir = path_identifier[ship_abbreviation]
    exists = os.path.isdir(datadir + '/' + cruise + '.tar')

    if exists and '-o' not in args:
        logging.info(datadir + '/' + cruise + '.tar exists')
    else:
        logging.info('Creating ' + datadir + '/' + cruise + '.tar')
        os.chdir('{}/{}'.format(datadir, cruise))
        os.system('chmod -R +rw ./*')  # changes permissions
        os.system('chgrp -R gdc ./*')
        os.chdir('{}'.format(datadir))  # moves into ship dir
        os.system('chmod 774 {}'.format(cruise))
        os.system('mkdir {}.tar'.format(cruise))  # makes tar dir

        # moves cruise dir into tar dir
        output = os.system('mv {} {}.tar'.format(cruise, cruise))
        if output != 0:
                logging.error('Could not move cruise directory')
                raise RuntimeError
        # moves into tar dir
        os.chdir('{}/{}.tar'.format(datadir, cruise))
        # creates an md5deep of cruise dir
        os.system('/mnt/gdc/bin/md5deep -c -r -l -o f -t -z . \
> ../{}.tar.md5deep'.format(cruise))
        logging.info('Finished running inventory on ' + cruise)
        if '-v' in args:
            print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                  'Finished running inventory on ' + cruise + '\n')


def create_md5deep(cruise):  # Ran with -m; Only if tar dir already exists
    """
    Generates an md5deep file from the cruise tar directory.

    cruise: A given cruise (matching a distro) to generate the md5deep from
    """
    logging.info(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                 'Creating md5deep for ' + cruise + '\n')
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              'Creating md5deep for ' + cruise + '\n')
    ship_abbreviation = get_ship_abbreviation(cruise.upper())
    datadir = path_identifier[ship_abbreviation]
    os.chdir('{}'.format(datadir))
    os.system('chmod -R +rw {}/*'.format(cruise))
    os.system('chgrp -R gdc {}/*'.format(cruise))
    os.system('/mnt/gdc/bin/md5deep -c -r -l -o f -t -z {} \
> ./{}.md5deep'.format(cruise, cruise))
    logging.info(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
                 'Finished creating md5deep for ' + cruise + '\n')
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              'Finished creating md5deep for ' + cruise + '\n')


def run_inventory_from_list(list):
    """
    Runs inventory given a newline separated list of cruises.

    list: A newline separated list of cruises
    """
    file = open('{}{}'.format(codedir, list), 'r')  # opens list of cruises
    list = [line.rstrip('\n') for line in file]  # splits cruises into a list
    print(list)
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Running inventory on cruises from list\n")
    logging.info("Running inventory on cruises from list")
    if '-m' in args:  # Use this flag if tar dir already exists
        for each in list:
            create_md5deep(each)
    else:
        for each in list:
            run_inventory(each)
    if '-v' in args:
        print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S: ') +
              "Script finished executing")
    logging.info("Script finished executing")


cruise = ''

for i in range(len(args)):
    if args[i][0] != '-' and args[i][0] != '.' and args[i][0] != '/':
        cruise = args[i]

os.chdir(log_dir)
logging.basicConfig(format='%(asctime)s %(message)s', filename='%s' %
                    (datetime.now().strftime('%Y-%m-%dT%H:%M:%S_') +
                     'run_inventory.py_' + cruise),
                    level=logging.INFO)
logging.info('run_inventory.py executed')

if '-l' in args:
    list = 'list.txt'
    #for i in range(len(args)):
        #if args[i][0] != '-' and args[i][0] != '.' and args[i][0] != '/':
            #list = args[i]
    run_inventory_from_list(list)
elif '-m' in args:
    create_md5deep(cruise)
else:
    run_inventory(cruise)
