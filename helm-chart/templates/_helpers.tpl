# helm-chart/templates/_helpers.tpl

{{/*
Expand the name of the chart.
*/}}
{{- define "kube-drift-agent.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "kube-drift-agent.fullname" -}}
{{- $name := default .Chart.Name .Values.fullnameOverride -}}
{{- printf "%s" $name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{/*
Create the name of the ServiceAccount to use
*/}}
{{- define "kube-drift-agent.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "kube-drift-agent.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default .Values.serviceAccount.name (include "kube-drift-agent.fullname" .) -}}
{{- end -}}
{{- end }}