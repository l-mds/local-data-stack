#!/bin/bash

source ./scripts/secops_config.sh

SOPS_AGE_RECIPIENTS=$(./scripts/simplify-public-keys.sh)
echo "recipient: ${SOPS_AGE_RECIPIENTS}"

for file in ${FILES_TO_ENCRYPT}; do
    echo "Encrypting: $file"
    sops --encrypt --age ${SOPS_AGE_RECIPIENTS} --input-type binary --output-type binary "$file" > "$file.enc"
done
