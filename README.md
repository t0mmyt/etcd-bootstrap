# Bring up a local cluster using docker-machine

1. Read Makefile

2. Run make

        ➜ make
        Attempting to start etcd on a (192.168.99.100)
        Attempting to start etcd on b (192.168.99.101)
        Attempting to start etcd on c (192.168.99.102)
        touch etcd-up

        ➜ etcdctl -version
        etcdctl version: 3.0.6
        API version: 2

        ➜ etcdctl --endpoints http://192.168.99.100:2379 cluster-health
        member c3bc806a49e1dd1 is healthy: got healthy result from http://192.168.99.102:2379
        member 8a3fa191d5488446 is healthy: got healthy result from http://192.168.99.101:2379
        member e1eeec531d5d33fa is healthy: got healthy result from http://192.168.99.100:2379

# Testing etcd failure scenarios

## TODO:

[X] &#10003; Node restart
[X] &#10005; Node comes back with same name but otherwise different
[ ] Same node goes away and comes back without data
[ ] Node goes down hard and is replaced (differnt IP, no data)

## Notes:

- Once a member is removed, it is permanent.  The node must be wiped of data and join as a new member
- Also, after removal, HTTP DELETE on token/node-id at discovery service
- A node cannot rejoin via discovery with the same name
