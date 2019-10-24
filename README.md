# Watchdog Keyhouse

This is the keyhouse repository required by SDSLabs Watchdog. This repository contains all the public keys of the members and the access right they have.

## How to use?

 - Keys are stored in `data/keys` file in the format `<username|keys>`.
 - To add your keys to keyhouse, you must create a PR. And wait for some admin to review it.
 - To gain access to any server, ask any admin.
 - To grant `uttu` access to `deploy@204`, add a new line `uttu|deploy` in `data/hosts/204`.
 - **Note:** `uttu` must have an entry in `data/keys` to gain access to any server.

