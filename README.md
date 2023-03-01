# flight-kubernetes

Example of building and deploying Apache Arrow Fligt to Kubernetes.
Includes examples of a Flight client in Python and Flight servers in Python and C++.

## Running

1. Build client and server images locally from the appropriate subfolder, e.g.,

    `nerdctl --namespace k8s.io build . -t flight-server:latest`
2. Apply K8s resource definitions from the appropriate subfolder

    `kubectl apply -f server.yml`
