#!/usr/bin/python

import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='Convert Ansible AWX/Tower Inventory to standard inventory')

parser.add_argument('--url', required=True, help='base url of AWX/Tower')
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('inventory', nargs=1, help='inventory name')

args = parser.parse_args()

r = requests.get('{}/api/v2/inventories/'.format(args.url), auth=(args.username, args.password))
iid = -1
for inventory in r.json()['results']:
    if inventory['name'] == args.inventory[0]:
        iid = inventory['id']
        break

if iid == -1:
    print("no such inventory")
    sys.exit(1)

r = requests.get('{}/api/v2/inventories/{}/script/?hostvars=1&towervars=1&all=1'.format(args.url, iid), auth=(args.username, args.password))


hosts = r.json()
for key in sorted(hosts):
    if key == 'all':
        continue
    if key == '_meta':
        continue
    if 'hosts' in hosts[key]:
        print('[{}]'.format(key))
        for host in hosts[key]['hosts']:
            print host
        print ''
    if 'children' in hosts[key]:
        print('[{}:children]'.format(key))
        for child in hosts[key]['children']:
            print child
        print ''
    if 'vars' in hosts[key]:
        print('[{}:vars]'.format(key))
        for var in hosts[key]['vars']:
            print '{}={}'.format(var, hosts[key]['vars'][var])
        print ''
    print ''
