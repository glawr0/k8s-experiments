# 001-build-web-app

First, we'll build a custom docker container and push it to a container registry. 

This example uses Python and the Flask framework to expose a very simple "Hello, World!" endpoint. 

Review the contents of the `app/` dir and the `Dockerfile` for more information. 

# Build the App

1) Check that the app can run locally:

```
poetry install 
poetry run gunicorn --bind=localhost:8080 wsgi:app 
curl http://localhost:8080/ 
```

2) Build the docker image:

```
docker build -t web-app .
```

3) Optionally, scan the docker image agains the Snyk vulnerability database:

```
docker scan web-app
```

Note that the majority of the vulnerabilities reported will be from the base Python image, rather than from the app code (or dependencies). 

4) Test that the new container can be run:

```
docker run -p 8080:8080 web-app
```

Note: `docker run` runs the container in the foreground. To launch the container in the background, run:

```
docker run -d -p 8080:8080 web-app
```

5) Now from your host, check that you can access the app in the container:

```
curl http://localhost:8080/
```

If you started the container as daemon, don't forget to stop the container:

```
docker ps
docker stop <CONTAINER_NAME>
```

# What's Next

You have successfully created a simple application which is packaged within a docker container. You have also been able to launch and test the container.

Next, we'll launch the container on Kubernetes (k8s) - a container orchestration platform.
