#!/usr/bin/env python
'''
Manipulate etcd on docker-machine
'''

import sh
from os import environ
import sys

# Container to use for etcd
ETCD = 'quay.io/coreos/etcd:v2.3.7'

if len(sys.argv) < 2 and sys.argv[1] not in ['start', 'stop']:
    print("Need start or stop")
    sys.exit(101)
action = sys.argv[1]

# Read discovery token (url)
try:
    with open('token') as f:
        discovery = f.read().rstrip()
except (OSError, IOError) as e:
    print("Couldn't open token: {}".format(e))
    sys.exit(102)


# Get IP addresses of DMs
mchn = dict([row.split(' ') for row in sh.docker_machine(
    'ls', '-f', '{{ .Name }} {{ .URL }}').rstrip().split('\n')])
for k, v in mchn.items():
    mchn[k] = (v[6:v.find(':', 6)])

# # Generate initial cluster string (not in use)
# initial_cluster = str.join(',', ["{}=http://{}:2380".format(k, m[k])
#                            for k in sorted(m.keys())])

# Get list of nodes to do
mchn_todo = sys.argv[2:] if len(sys.argv) > 2 else sorted(mchn.keys())

def etcd_srv(ip, domain, name):
    sh.docker('run', '-d', '--name', 'etcd',
        '-p', '2379:2379', '-p', '2380:2380',
        '-v', '/etc/ssl/certs/:/etc/ssl/certs',
        ETCD, '--name', "{}.{}".format(name, domain),
        '--advertise-client-urls', 'http://{}:2379'.format(ip),
        '--initial-advertise-peer-urls', 'http://{}.{}:2380'.format(name,domain),
        '--listen-peer-urls', 'http://0.0.0.0:2380'.format(name,domain),
        '--listen-client-urls', 'http://0.0.0.0:2379',
        '--discovery-srv', domain,
        '--initial-cluster-state', 'new',
    )


for k in mchn_todo:
    for e in filter(lambda x: len(x) > 0 and x[0:7] == 'export ',
                    sh.docker_machine('env', k).split('\n')):
        environ[e[7:e.find('=')]] = e[e.find('=')+1:].strip('"')

    print('Attempting to {} etcd on {} ({})'.format(action, k, mchn[k]))
    if action == 'start':
        ip = mchn[k]
        etcd_srv(ip, 'test.kube.usw.co', k)
    elif action == 'stop':
        sh.docker('rm', '-f', 'etcd')

#sh.docker('run', '-d', '--name', 'etcd',
#          '-p', '2379:2379', '-p', '2380:2380',
#          '-v', '/etc/ssl/certs/:/etc/ssl/certs',
#          ETCD, '--name', k,
#          '--advertise-client-urls', 'http://{}:2379'.format(ip),
#          '--listen-client-urls', 'http://0.0.0.0:2379',
#          '--initial-advertise-peer-urls', 'http://{}:2380'.format(ip),
#          '--listen-peer-urls', 'http://0.0.0.0:2380',
#          '--initial-cluster-token', 'etcd-test-cluster',
#          '--discovery', discovery)
# # Alternate bootstrap if nodes known. (not using discovery)
# sh.docker('run', '-d', '--name', 'etcd',
#           '-p', '2379:2379', '-p', '2380:2380',
#           etcd, '--name', k,
#           '--advertise-client-urls', 'http://{}:2379'.format(ip),
#           '--listen-client-urls', 'http://0.0.0.0:2379',
#           '--initial-advertise-peer-urls', 'http://{}:2380'.format(ip),
#           '--listen-peer-urls', 'http://0.0.0.0:2380',
#           '--initial-cluster-token', 'etcd-test-cluster',
#           '--initial-cluster', initial_cluster,
#           '--initial-cluster-state', 'new')
