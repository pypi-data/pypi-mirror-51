# deploy

Basic usage:

```
deploy --staging
```

or

```
deploy --production
```

in the application root directory.

### Usage

Usage:

```
usage: deploy.py [-h] [--force] [--build] [--push] [--production] [--staging]
                 [--promote] [--tag {commit_hash,date}]
                 [service]

Deploy the application.

positional arguments:
  service               Service to deploy

optional arguments:
  -h, --help            show this help message and exit
  --force, -f           Force deploy. It's probably a bad idea.
  --build, -b           Only build images
  --push                Build and push images
  --production, -p      Build, push and redeploy images TO PRODUCTION
  --staging, -s         Build, push and redeploy images to the staging
                        environment
  --promote, -P         Promote image from staging to the production
                        environment
  --tag {commit_hash,date}, -t {commit_hash,date}
                        How to name a docker image.
```
