#!/bin/sh

#DOC
#https://eu-west-1.console.aws.amazon.com/ecr/repositories/private/606119601477/hanka-beton?region=eu-west-1

#login
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 606119601477.dkr.ecr.eu-west-1.amazonaws.com

#image
docker build -t hanka-beton .
docker tag hanka-beton:latest 606119601477.dkr.ecr.eu-west-1.amazonaws.com/hanka-beton:latest
docker push 606119601477.dkr.ecr.eu-west-1.amazonaws.com/hanka-beton:latest

