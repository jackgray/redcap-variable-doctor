#!/bin/env bash

# version=2.0.0
# appname=redcap_variable_doctor

image=jackgray/${appname}:${version}

docker buildx -t ${image} .

docker push ${image}
