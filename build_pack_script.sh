#!/bin/bash

dev_install () {
    yum -y update
    yum -y upgrade
    yum -y groupinstall "Development Tools"
    yum install -y findutils zip
    yum install -y python36-devel python36-virtualenv
}

make_virtualenv () {
    cd /home
    rm -rf env
    python3 -m virtualenv env --python=python3
    source env/bin/activate
}

install_pytorch () {
    pip install http://download.pytorch.org/whl/cpu/torch-0.3.0.post4-cp36-cp36m-linux_x86_64.whl 
    pip install torchvision
}

install_packages () {
    pip install -r /host/requirements.txt
}

gather_pack () {
    cd /home
    rm -rf lambdapack
    mkdir lambdapack
    cd lambdapack

    # Copy python pakages from virtual environment
    cp -R /home/env/lib/python3.6/site-packages/* .
    cp -R /home/env/lib64/python3.6/site-packages/* .
    
    echo "Original size $(du -sh /home/lambdapack | cut -f1)"

    # Clean pakages
    find . -type d -name "tests" -exec rm -rf {} +
    find -name "*.so" | xargs strip
    find -name "*.so.*" | xargs strip
    rm -r pip
    rm -r pip-*
    rm -r wheel
    rm -r wheel-*
    rm easy_install.py
    find . -name \*.pyc -delete
    echo "Stripped size $(du -sh /home/lambdapack | cut -f1)"

    # Compress
    zip -FS -r1 /host/pack.zip * > /dev/null
    echo "Compressed size $(du -sh /host/pack.zip | cut -f1)"
}

add_pack () {
    cd /host

    cp /host/lambda_function.py /home/lambdapack/.
    zip -9 -q -r pack.zip lambda_function.py

    cp /host/model.py /home/lambdapack/.
    zip -9 -q -r pack.zip model.py
}

main () {
    dev_install
    make_virtualenv
    install_pytorch
    install_packages
    gather_pack
    add_pack
}

main