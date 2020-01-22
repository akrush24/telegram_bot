# tBot

## k8s

### first create secret from passwd.py
```# kubectl create secret generic tbot-passwd.py --from-file=./passwd.py```

### create haproxy ConfigMap for telegram proxy
```# kubectl create configmap tbot-haproxy-config --from-file ./haproxy/haproxy.cfg```
