DRIVER ?= virtualbox
NODES ?= {a..c}

all: dm-up etcd-up

clean: etcd-down dm-down
	rm -f token

token:
	curl -s --fail "https://discovery.etcd.io/new?size=3" > token

dm-up:
	for i in ${NODES} ; do \
		docker-machine create --driver=${DRIVER} --virtualbox-memory 512 $$i ; \
	done && touch dm-up

dm-down:
	for i in ${NODES}; do \
		docker-machine rm -f $$i; \
	done
	rm -f dm-up

etcd-up: dm-up token
	python etcd.py start
	touch etcd-up

etcd-down:
	python etcd.py stop
	rm -f etcd-up
