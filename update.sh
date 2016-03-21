#!/bin/bash

rm -rf bucksbuddy
rm bucksbuddy-v1.zip 
../google_appengine/endpointscfg.py get_client_lib java -bs gradle -o .  bucksbuddy.BucksBuddyApi
unzip bucksbuddy-v1.zip 
cd bucksbuddy
gradle install
cd ..
