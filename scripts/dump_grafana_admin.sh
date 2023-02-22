#!/bin/sh
#
kubectl get secret --namespace default kube-prometheus-stack-1676593573-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
