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


{{/*
Generte the Ingress nginx cors
*/}}
{{- define "phoenixmain.ingress_cors" -}}
{{- if .Values.ingress_cors.enabled }}
nginx.ingress.kubernetes.io/enable-cors: "true"
nginx.ingress.kubernetes.io/cors-allow-origin: {{ tpl .Values.ingress_cors.allow_origin . }}
{{- end }}
{{- end -}}

{{/*
Phiphi container
*/}}
{{- define "phoenixmain.phiphi_container" -}}
image: {{ tpl (.Values.api.image.repository ) . }}:{{ tpl (.Values.api.image.tag) . }}
imagePullPolicy: {{ .Values.api.image.pullPolicy }}
ports:
  - containerPort: 80
env:
  - name: IMAGE_URI
    value: {{ tpl .Values.api.image.repository . }}:{{ tpl .Values.api.image.tag . }}
  - name: PHIPHI_LOG_CONFIG
    value: {{ .Values.api.phiphiLogConfig | quote }}
  - name: SQLALCHEMY_DATABASE_URI
    valueFrom:
      secretKeyRef:
        name: {{ tpl ( .Values.api.secretKey ) . }}
        key: SQLALCHEMY_DATABASE_URI
  - name: CORS_ORIGINS
    value: {{ tpl ( .Values.api.cors_origins ) .}}
  - name: FIRST_ADMIN_USER_EMAIL
    value: {{ .Values.api.first_admin_user_email | quote }}
  - name: FIRST_ADMIN_USER_DISPLAY_NAME
    value: {{ .Values.api.first_admin_user_display_name | quote }}
  - name: HEADER_AUTH_NAME
    value: {{ .Values.api.header_auth_name | quote}}
  # There are alot of problems with setting the forwarded allow ips when used in the cli command.
  # For instances you have to do `--forwarded-allow-ips=*` with no quotes (double or single) around the *
  - name: FORWARDED_ALLOW_IPS
    value: {{ .Values.api.forwarded_allow_ips | quote}}
  - name: USE_MOCK_APIFY
    value: {{ .Values.api.use_mock_apify | quote }}
  - name: VERSION
    value: {{ tpl (.Values.api.version) . | quote }}
  - name: INCLUDE_INSECURE_AUTH
  {{- if .Values.use_local_insecure_auth }}
    value: "true"
  {{- else }}
    value: "false"
  {{- end }}
  {{- if .Values.gcp_service_account.enabled }}
  - name: GOOGLE_APPLICATION_CREDENTIALS
    value: /var/secrets/google/{{ .Values.gcp_service_account.secret_key }}
  {{- end }}
  {{- if .Values.api.apify_api_keys.enabled }}
  - name: APIFY_API_KEYS
    valueFrom:
      secretKeyRef:
        name: {{ tpl ( .Values.api.apify_api_keys.secret_name ) . }}
        key: {{ .Values.api.apify_api_keys.secret_key }}
  {{- end }}
  {{- if and .Values.prefect .Values.prefect.apiKey }}
  - name: PREFECT_API_KEY
    valueFrom:
      secretKeyRef:
        name: prefect-api-key
        key: key
  {{- end }}
  {{- if index (index .Values "prefect-worker" ) "enabled" }}
  - name: PREFECT_API_URL
    # This uses the subchart to get the prefect-worker url
    value: {{ include "worker.apiUrl" (index  .Subcharts "prefect-worker") }}
  {{- end }}
  {{- if .Values.api.bqDefaultLocation }}
  - name: BQ_DEFAULT_LOCATION
    value: {{ .Values.api.bqDefaultLocation | quote }}
  {{- end }}
  {{- if .Values.api.prefectLoggingSettingsPath }}
  - name: PREFECT_LOGGING_SETTINGS_PATH
    value: {{ .Values.api.prefectLoggingSettingsPath | quote }}
  {{- end }}
## This is the secret that is used to store the GCP service account json
{{- if .Values.gcp_service_account.enabled }}
volumeMounts:
- name: gcp-creds
  mountPath: /var/secrets/google
  readOnly: true
{{- end }}
{{- end -}}
