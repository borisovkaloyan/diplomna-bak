python setup.py sdist bdist_wheel
gcloud builds submit --region=us-west2 --tag us-west2-docker.pkg.dev/parkingbuddy-424610/quickstart-docker-repo/backend:1.0.0
