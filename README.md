# Telegram Bot



## Please run it in Kubernetes, run it in kubernetes is best practice =)

### first create secret from passwd.py

```# kubectl create secret generic tbot-passwd.py --from-file=./passwd.py```

example my passwd.yaml is:
```$ cat ./passwd.example.py```

### create haproxy ConfigMap for telegram proxy
For telegram proxy I use my own proxy servers (one in Germany one in Amsterdam). To balance traffic, I use HaProxy.

```# kubectl create configmap tbot-haproxy-config --from-file ./haproxy/haproxy.cfg```

example my HaProxy config is: 
```$ cat haproxy/haproxy.cfg```

### Check: ###
```
# kubectl get deployments tbot-deployment
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
tbot-deployment   1/1     1            1           17d
# kubectl get pod tbot-deployment-84cc9fdb5d-96srj
NAME                               READY   STATUS    RESTARTS   AGE
tbot-deployment-84cc9fdb5d-96srj   4/4     Running   77         2d11h
# kubectl get secrets tbot-passwd.py
NAME             TYPE     DATA   AGE
tbot-passwd.py   Opaque   1      125d
# kubectl get secrets tbot-ssh-key
NAME           TYPE     DATA   AGE
tbot-ssh-key   Opaque   2      169d
# kubectl get configmaps tbot-haproxy-config
NAME                  DATA   AGE
tbot-haproxy-config   1      4d6h
```
