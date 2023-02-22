#!/bin/sh

export POD_NAME=`kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}"`
 kubectl --namespace default port-forward $POD_NAME 3000
