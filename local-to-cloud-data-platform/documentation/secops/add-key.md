# Add key for age encryption

example how to create a public/private pair for age based encryption

## creating the keys for the new user

The new user executes:

```bash
age-keygen -o key.txt
```

The new user creates a pull request to add his/her public key to the file.

> Ensure that the key is added to the list of [public age keys](public-keys.txt).
> Keys are comma separated - just add a new line and describe the owner/person for that key.

> Ensure all files to be encrypted are listed in [secops_config.sh][scripts/secops_config.sh]

Do not forget to re-encrypt all the secrets for this new user.


The `key.txt` file should be placed at the root of the repository.


## encrypting/decrypting 

To en-/decrypt:

```bash
pixi run secrets-encrypt
pixi run secrets-decrypt
```