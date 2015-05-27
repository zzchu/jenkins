#!/bin/bash

#WME pipeline xcode update may be ahead of spark client pipeine environment update 
if [ "${SDK_VERSION}" == "" ]
then
    export SDK_VERSION=8.3
fi

echo "Running with iOS ${SDK_VERSION} SDK..."
