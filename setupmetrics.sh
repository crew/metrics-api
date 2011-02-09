#!/bin/bash

# Path to the virtualenv executable
VENV=/usr/bin/virtualenv
SCRATCH_DIR=/scratch/$USER
ENVDIR_NAME=metricsenv
ENVDIR=$SCRATCH_DIR/$ENVDIR_NAME

mkdir metrics

pushd metrics
for x in api frontend backend aggregator; do
    # if the subdirectory does not exist, git clone it.
    if [ ! -d $x ] ; then
        git clone git@crew-git.ccs.neu.edu:metrics/$x.git
    fi
done
popd

# if the env directory does not exist, virtualenv it.
if [ ! -d $ENVDIR ] ; then
    $VENV $ENVDIR
fi

# Setup symlinks to the virtualenv directory.
echo "Setting up symlinks"
for x in api frontend backend aggregator; do
    pushd metrics/$x
    ln -s $ENVDIR env
    popd
done

echo "Enabling virtualenv"
source $ENVDIR/bin/activate || echo "Unable to enable virtualenv." || exit 1

echo "Setting up."
# Install pip, because the requirements files need this.
easy_install pip

echo "Installing api."
pushd metrics/api; python setup.py install; popd

echo "Installing frontend dependencies"
pushd metrics/frontend; pip install -r requirements.txt; popd

echo "Installing backend dependencies"
pushd metrics/backend
pip install -r requirements.txt
echo "Installing backend."
python setup.py install
popd

echo
echo "*** REMINDER: run the following. ***"
echo "source $ENVDIR/bin/env/activate"
