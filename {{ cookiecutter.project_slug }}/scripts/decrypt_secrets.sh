#!/bin/bash

source ./scripts/secops_config.sh

export SOPS_AGE_KEY_FILE=key.txt

for file in ${FILES_TO_ENCRYPT}; do
    echo "Decrypting: $file"
    sops --decrypt --input-type binary --output-type binary "$file.enc" > "$file"
done
