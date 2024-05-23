# Local with authentication 

This local cluster will set up the phoenix platform with:
- autentication to the dev buildup auth0 authentication app
- ssl with self signed certificates

## Running
It can be run with:
```
source setup_microk8s.sh
make local_with_auth_up
```

You will need to:
- follow the instructions to set up your `/etc/hosts` file
- set up the secrets in `cluster/local_with_auth/secrets.yaml` file to include the auth0 client id
  and secret.

You will then need to visit the following urls and proceed with the insecure certificate. Be aware
the you may need to log in at some point:
- [https://oauth.phoenix.local/](https://oauth.phoenix.local/)
- [https://api.phoenix.local/](https://api.phoenix.local/)
- [https://console.phoenix.local/](https://console.phoenix.local/)
