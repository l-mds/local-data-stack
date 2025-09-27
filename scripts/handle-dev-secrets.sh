#!/bin/bash

cp key.txt rendered-template/local_data_stack/
cd rendered-template/local_data_stack
make secrets-decrypt
cd ../../