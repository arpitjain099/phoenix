# Phoenix helm chart main

This is the main helm chart for Phoenix. It is a collection of subcharts that are used to deploy Phoenix.

## Subcharts

- [Superset](https://github.com/apache/superset/tree/master/helm/superset)
- [Oauth2 Proxy](https://github.com/oauth2-proxy/manifests/tree/main/helm/oauth2-proxy)
- [cert-manager](https://artifacthub.io/packages/helm/cert-manager/cert-manager)


## SSL Certificates

The chart uses [cert-manager](https://cert-manager.io/docs/) for SSL certification creation. It is
disabled by default.

To set up the certifications for a deployment:

* Release the chart with the `cert-manager.enabled` set to `false`
* Set up the dns records for the domain so that the domain points to the load balancer/ingress
* Enable cert-manager and config cert issuer by setting `cert-manager.enabled` and
  `cert_issuer.enabled` to `true` and other values in `cert_issuer`. See the
  [values.yaml](values.yaml) for the options.
* Set the `cert_issuer.issuer_name` to the name of the issuer `letsencrypt-staging`
* Check that the certificates are created and "READY" by running `kubectl get certificates -A`
* If they are ready you can use `cert_config.issuer_name` to `letsencrypt-prod` to get the production
  certificates
* You can then visit the https://<domain> and see the certificates are valid

## Gotchas

Be aware that you can only that in the docs of the [helm
chart](https://cert-manager.io/docs/installation/helm/):

> Be sure never to embed cert-manager as a sub-chart of other Helm charts; cert-manager manages
> non-namespaced resources in your cluster and care must be taken to ensure that it is installed
> exactly once.

This means that if you should be careful when using `cert-manager.enabled: true` as there should
only be on cert-manager in the cluster. If you have more complex setups you should install
`cert-manager` as a separate helm chart.
