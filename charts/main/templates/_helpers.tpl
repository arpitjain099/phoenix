{{/*
Define scheme based on cert_issuer.enabled
*/}}
{{- define "phoenixmain.scheme" -}}
{{- if .Values.cert_issuer.enabled -}}
https
{{- else -}}
http
{{- end -}}
{{- end -}}

{{/*
Generate auth-signin annotation value
*/}}
{{- define "phoenixmain.authSignin" -}}
nginx.ingress.kubernetes.io/auth-signin: {{ include "phoenixmain.scheme" . }}://oauth.{{ .Values.base_host }}/oauth2/start?rd={{ include "phoenixmain.scheme" . }}://$host$uri
{{- end -}}
