# Watchdog Keyhouse

This is the keyhouse repository required by SDSLabs Watchdog. This repository contains all the public keys of the members and the access right they have.

## How to use?
 - List of servers is in `config.json`
 - Public keys are stored in `data/keys` file.
 - To add your keys to keyhouse, you must create a PR. And wait for some admin to review it.
 - To gain access to any server, ask any admin.
 - To grant `<user>` access to `<group>` in `<server>`, add a new line `<server>|<group>` in `data/hosts/<user>`.
 - For example, to grant `saturn` access to `sudo` group in `aws` server, add a new line `aws|sudo` in `data/hosts/saturn`.
 - **Note:** users must have an entry in `data/keys` to gain access to any server.