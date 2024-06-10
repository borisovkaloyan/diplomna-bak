# diplomna-bak
Parking buddy Diploma.
Consists of a FastAPI backend for storing user and license data, Mobile application in .NET MAUI and a Computer Vision number plate recognition.

# Backend
Backend Database is hosted on Aiven at 'parking-parking-thing-2024.l.aivencloud.com\
Port is 15672\
User is 'avnadmin'\
Pass is 'AVNS_QHiicYULKpnh43AE64Z'\
Database name is 'defaultdb'

Backend is hosted on Google Cloud at [34.118.78.253](http://34.118.78.253/)
Uses a Kubernetes cluster.

Upgrade Container image:
Build image with build.bat, then use kubectl in deployment
```kubectl set image deployment/parkingbuddy backend-sha256-1=us-west2-docker.pkg.dev/parkingbuddy-424610/quickstart-docker-repo/backend:1.0.5```

Enable/Disable service:
```kubectl scale deployment/parkingbuddy --replicas=0```
replicas set to 1 for enable, 0 for disable
