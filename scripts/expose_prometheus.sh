#/bin/sh
#

#ui
export POD_NAME=`kubectl get pods --namespace default -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}"`
kubectl --namespace default port-forward $POD_NAME 9090

# gateway

export POD_NAME=`kubectl get pods --namespace default -l "app=prometheus-pushgateway,component=pushgateway" -o jsonpath="{.items[0].metadata.name}"`
kubectl --namespace default port-forward $POD_NAME 9091

