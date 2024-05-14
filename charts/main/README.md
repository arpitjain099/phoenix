# Phoenix helm chart main

This is the main helm chart for Phoenix. It is a collection of subcharts that are used to deploy Phoenix.

## Subcharts

- [Superset](https://github.com/apache/superset/tree/master/helm/superset)
- [Oauth2 Proxy](https://github.com/oauth2-proxy/manifests/tree/main/helm/oauth2-proxy)
- [cert-manager](https://artifacthub.io/packages/helm/cert-manager/cert-manager)

## Secrets

Currently secrets for the chart are not stored in the chart. The expectations is that Secret
resource should be created in the cluster. The secrets should be created in the namespace that the
chart is deployed in.

See the [example_secrets.yaml](example_secrets.yaml) for the secrets that are expected.


## SSL Certificates

The chart uses [cert-manager](https://cert-manager.io/docs/) for SSL certification creation. It is
disabled by default.

Although this chart contains a cert-manager as a subchart it is not enabled by default. This is
recommended that you DO NOT install the cert-manager as a subchart. Instead you should install
cert-manager as a separate helm chart. See [cert-manager
docs](https://cert-manager.io/docs/installation/helm/).

To set up the certifications for a deployment:

* Release the chart with the `cert-manager.enabled` and `cert_issuer.enabled` set to `false`
* Set up the dns records for the domain so that the domain points to the load balancer/ingress
* ONLY if for testing: Enable cert-manager `cert-manager.enabled` and install
* Once the cert-manager is installed set the `cert_issuer.enabled` to `true` and other values in
  `cert_issuer`. See the [values.yaml](values.yaml) for the options.
* Set the `cert_issuer.issuer_name` to the name of the issuer `letsencrypt-staging`
* Check that the certificates are created and "READY" by running `kubectl get certificates -A`
* If they are ready you can use `cert_config.issuer_name` to `letsencrypt-prod` to get the production
  certificates
* You can then visit the https://<domain> and see the certificates are valid

## Authentication

The chart uses [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) for authentication. It
can be configured to use a variety of authentication providers.

Be aware that the configuration of the cookie can be some what complex. For instance:
- http-only cookies can not be seen by javascript. This needs to be false to use
  `console.env_auth_cookie= "_oauth2_proxy"`
- secure means that the cookie can only be sent over https
- same-site "strict" and "lax" cookies can mean that a console on a different domain will not have
  the cookies
- same-site "none" cookies can be used for cross-site cookies but require the secure flag to be set
  on the cookie

### Insecure authentication for local testing

The chart can be configured to use an insecure authentication. This is useful for testing and
should not be used for production. See the [./values.yaml](./values.yaml) for the options.

## CORS

Their are a number of complexities with CORS. In that for the console to work the CORS for the
ingress (oauth and general) and the API need to be set up so that the site URL that the console is
served from is an allowed origin for the ingress and the API. Be careful to use the correct schema
(http|https). See [./values.yaml](./values.yaml) for the options.
