# 002-deploy-web-app

This module will deploy the container we created in module 001. We will use Kubernetes (k8s for short), a production-grade industry standard container orchestration tool. 

k8s provides some powerful features, like automated application rollouts, self-healing and scaling.

In this module we'll deploy the container as-is. This will serve traffic over HTTP running on port 8080. 
In subsequent modules, we'll utilize k8s features and patterns to make the application production-ready. 

# Pre-Requisites

You must have a Kubernetes cluster installed on your local machine. See Module 000 for more instructions.

To validate your cluster, run:

```
kubectl cluster-info
```

This should return something like:

```
Kubernetes control plane is running at https://kubernetes.docker.internal:6443
CoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

# Getting Started


