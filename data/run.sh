#!/bin/bash
docker run -it --name lambdapack10 -v $(pwd):/host amazonlinux:latest /bin/bash /host/build_pack.sh