#!/usr/bin/env bash

set -e

docker run -d --name dsapi -p 5000:5000 361421599476.dkr.ecr.ap-southeast-1.amazonaws.com/sastaticket-prod:latest
