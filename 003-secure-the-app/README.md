# 003-secure-the-app

In this module, we'll use the Caddy webserver to secure the app using Transport Layer Security (TLS). 

We will achieve this by using a common cloud pattern called a Sidecar. A Sidecar is an additional container which is deployed alongside the application container (web-app, in our case). The Sidecar provides additional new features without having to modify the original application container code. Your "pure" application code, or business logic, can be isolated from all this annoying "DevOps" stuff. Neat, huh?


## Build Caddy Image

Caddy uses a simple configuration called a `Caddyfile` to configure the webserver. 

1) Review the Caddyfile and Dockerfile and see what is happening. To allow for easy testing, we'll add a simple static index.html. All other requests will be proxied to whatever service is running on 127.0.0.1:8080. This will be our application container running web-app, but caddy doesn't care about that!

2) Build the custom caddy image. First, set some environment vairables. Modify them as appropriate:

```
export DOCKER_HUB_USERNAME=gedlawrenson
export CONTAINER_NAME=caddy-sidecar
export CONTAINER_VERSION=v1.1
```

Next, run these commnads to build and publish the new container to Docker Hub:

```
cd caddy
docker build -t ${CONTAINER_NAME} .
docker tag caddy-sidecar ${DOCKER_HUB_USERNAME}/${CONTAINER_NAME}:${CONTAINER_VERSION}
docker push ${DOCKER_HUB_USERNAME}/${CONTAINER_NAME}:${CONTAINER_VERSION}
```
 
Meta Note: Separating out user-specified commands from generic commands makes it simple to build Runbooks. This reduces the effort required for your friends or colleagues to get up to speed with your project. 

3) Check that your new caddy-sidecar runs in isolation:

```
docker run -p 443:443 caddy-sidecar
curl https://localhost/index.html
```

You should see "Hello, from Caddy!" 

4) Now create the web-app-deployment and caddy-sidecar-service.

```
cd ..
kubectl apply -f web-app-deployment.yml
kubectl apply -f caddy-sidecar-service.yml
```

5) Now test your new configuration:

```
curl -k https://localhost/index.html
curl -k https://localhost/
```

The first command should return "Hello, from Caddy!".
The second command should return "Hello, World!". 

What is happening is that the Service finds the Pod(s) matching the specified selector label (web-app) and routes traffic on Port 443. 
The traffic on Port 443 is recieved by the caddy-sidecar (which is listening on 443). 
The Caddy sidecar configuration can either return the static index.html, or reverse proxy traffic to 127.0.0.1:8080 - which happens to be the IP & port that the web-app container is listening on!


## Cleanup

```
kubectl delete -f caddy-sidecar-service.yml
kubectl delete -f web-app-deployment.yml
```

## What's Next?

Well done, you've got everything working locally using the Sidecar. This is a great achievement, but you may have already noticed some issues with this approach. 

Doing things locally is great to get started, but it can be frustrating to setup your environment correctly and having to run commands manually to make changes to your images. 

Caddy also introduces something else for us to manage and worry about. You probably aren't an expert in Caddy, you're an expert in the problem you are trying to solve. It would be nicer if we could get Kubernetes to take care of these lower level concepts like traffic routing and TLS. 

Lastly, something that runs on your laptop - even if it is using Kubernetes - is not particularly resilient. Using a managed Kubernetes service can help you to sleep better at night and to improve your application availability. 

So, next up we'll look at:

    * Using Github Actions to build new Docker images whenever you push to Github.
    * Deploying your app to someone else's Kubernetes infrastructure.
    * Taking advantage of Kubernetes native ingress controllers.