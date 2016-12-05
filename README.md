# Bring up a local cluster using docker-machine

1. Read Makefile

2.
        ➜ make
        Attempting to start etcd on a (192.168.99.100)
        Attempting to start etcd on b (192.168.99.101)
        Attempting to start etcd on c (192.168.99.102)
        touch etcd-up

        ➜ etcd-bootstrap λ etcdctl -version
        etcdctl version: 3.0.6
        API version: 2

        ➜ etcd-bootstrap λ etcdctl --endpoints http://192.168.99.100:2379 cluster-health
        member c3bc806a49e1dd1 is healthy: got healthy result from http://192.168.99.102:2379
        member 8a3fa191d5488446 is healthy: got healthy result from http://192.168.99.101:2379
        member e1eeec531d5d33fa is healthy: got healthy result from http://192.168.99.100:2379
