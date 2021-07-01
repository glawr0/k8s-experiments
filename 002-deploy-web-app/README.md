# 002-deploy-web-app

## Module Overview
This module will deploy the container we created in module 001. We will use Kubernetes (k8s for short), a production-grade industry standard container orchestration tool. 

k8s provides some powerful features, like automated application rollouts, self-healing and scaling.

In this module we'll deploy the container as-is. This will serve traffic over HTTP running on port 8080. 
In subsequent modules, we'll utilize k8s features and patterns to make the application production-ready. 

First, let's get up to speed with some basic k8s terminology. 

## k8s Terminology

* Cluster - A k8s cluster consists of both a Controler Plane and atleast one Worker Node
* Control Plane - The Control Plane is the management interface for k8s Cluster. It is responsible for the management of containers. 
* Node - A node is a machine which runs application workloads. 
* Pod - A Pod contains one or more application containers which are co-located. Pods are logically isolated from one another, however containers within a pod share network and storage resources. A Pod is typically created by a Workload Resource, such as a Deployment. Pods can be replicated for resiliency by using ReplicaSets. 
* ReplicaSets - A ReplicaSet ensures that the desired number of Pods is running for a particular application. 
* Deployment - A Deployment defines how an application is deployed to the underlying Pod or ReplicaSet. 
* Service - A Service is an abstraction used to provide load-balanced network access to a set of Pods. 


## Pre-Requisites

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

## Getting Started

1) Create a Kubernetes Deployment for the web-app. Review the `web-app-deployment.yml` file. This file will create a ReplicaSet containing three replicas. Three Pods will be created which will run the `<YourDockerHubUsername>/web-app:v1` image. 

```
kubectl apply -f web-app-deployment.yml
```

2) Use the following commands to check the health of the Deployment, ReplicaSet and Pod:

```
kubectl get deployments
kubectl get replicasets
kubectl get pods
```

You should see that there is a single `web-app-deployment`, comprised of one ReplicaSet. The ReplicaSet will have a desired value of 3 Pods, with 3 Pods in the 'Ready' state. Each Pod should contain 1 running instance. 



## What's Next?
