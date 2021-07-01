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

## Create a Deployment 

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

You should see that:

* There is a single `web-app-deployment`, comprised of one ReplicaSet. 
* The ReplicaSet will have a desired value of 3 Pods, with 3 Pods in the 'Ready' state. 
* Each Pod should contain 1 running instance. 

Each Pod has it's own internal IP address, which is visible using `kubectl get pods -o wide`. We'll need to create a Service object to expose the Pods and the app externally.

## Create a Service

A Service provides external access to Pods. The Pods are selected using a Label selector. 

1) Create a Service for the web-app. Review the `web-app-service.yml` file. This file will create a LoadBalancer Service which will expose any Pods which use the `web-app` label. Traffic will be exposed externally on port 80 and will be routed internally to the Pods on port 8080. 

User ---\[HTTP TCP/80]---> K8s Service ---\[HTTP TCP/8080]---> Pod

```
kubectl apply -f web-app-service.yml 
```

2) Inspect the new service to confirm the EXTERNAL-IP:

```
kubectl get service web-app-service
```

NAME              TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)        AGE
web-app-service   LoadBalancer   10.98.3.15   localhost     80:32386/TCP   4s

3) Now try to access the application from your local machine. Remember to use Port 80 this time instead of 8080:

```
curl http://localhost:80/
```

## What's Next?

You've successfully deployed an application to Kubernetes and configured a simple loadbalancer to route external traffic to the app. Pat yourself on the back!

This setup provides some limited availability benefits:
* If your app becomes unhealthy, k8s will terminate the Pod and create a new one automatically. 
* Your app is being automatically loadbalanced between the 3 Pods.

However, there are definitely some improvements to be made:
* All 3 Pods are still deployed on the same physical Node. If the Node were to fail for some reason, your app would become unavailable!
* If you deploy an update to the app, there will be some downtime. 'Big Bang' deployments are to be avoided. 

Next up in Module 003, we'll look at how to improve the security of your application by protecting it with Transport Layer Security (TLS). We'll also see how to do this without making changes to the application container, by using a handy pattern called a Sidecar Proxy. 
