# Hello-Enclaive - Kubernetes / Helm Challenge

FastAPI service on a 3-node cluster, deployed via Helm with Prometheus monitoring and Vault secret injection.
Fully reproducible via helm/kubectl - no manual changes.


## Prerequisites

k8s cluster (3 nodes), helm, kubectl, docker.
First node has taints: `kubectl taint nodes minikube key=critical:NoSchedule` that restricts workload pod placement by default.

Example:
```bash
minikube start --nodes 3 --cni=calico --driver=docker
kubectl taint nodes minikube key=critical:NoSchedule
```

## 1. Build Docker locally
- `app/build.sh` - script execution creates 2 images with `latest` tag and `GIT_HASH` tag and deliver to cluster

Example:
```bash
docker save app:latest -o /tmp/app.tar
for n in $(minikube node list | awk '{print $1}'); do
    minikube cp /tmp/app.tar "$n:/tmp/app.tar" && minikube ssh -n "$n" -- docker load -i /tmp/app.tar
done
```

## 2. Deploy Helm charts
```bash
helm upgrade --install vault charts/vault -n vault --create-namespace --wait --timeout 5m && \
helm upgrade --install monitoring charts/monitoring -n monitoring --create-namespace && \
helm upgrade --install app charts/app -f charts/app/values.dev.yaml -n dev --create-namespace --wait --timeout 5m && \
helm upgrade --install app charts/app -f charts/app/values.prod.yaml -n prod --create-namespace --atomic --timeout 5m
```

Check endpoinds in browser or by curl.
Example:
```bash
curl $(minikube ip):30000/healthz -> {"SYS_ENV":"hello-enclaive"} #dev
curl $(minikube ip):30001/healthz -> {"SYS_ENV":"hello-enclaive"} #prod
```

## 3. Perform Rollback
- `helm rollback app -n prod` - rollback helm release to previous revision
- `helm history app -n prod` - get desired revision number
- `helm rollback app <REVISION_NUMBER> -n prod` - rollback to desired revision number

## 4. Access metrics

### Port forwarding:
```bash
kubectl port-forward -n monitoring svc/monitoring-prometheus-server 9090:80
kubectl port-forward -n monitoring svc/monitoring-alertmanager 9093:9093
```

### Simulate PodCrashLoop:
- `kubectl create deployment crashloop -n dev --image=busybox -- /bin/sh -c "exit 1"` - create broken pod
- watch http://localhost:9093/#/alerts in next ~2 min

## 5. Tricky tainted node:

To allow *prod* workload placements on first node pod `spec.template.spec.tolerations` is used:
```yaml
...
      {{- if eq .Values.environment "prod" }}
      tolerations:
        - key: "key"
          operator: "Equal"
          value: "critical"
          effect: "NoSchedule"
      {{- end }}
...
```

## Security notes

For challenge:
- Vault in dev mode: in-memory, root token `root`
- Secret value and root token live in the chart that is ok because of `hello-enclaive` is a dummy
- Plain HTTP in-cluster, no TLS
- App is hardened (non-root, readOnlyRootFilesystem, dropped caps, dedicated SA, secret via tmpfs)

For real production: Vault (persistent + auto-unseal, secret out of git), NetworkPolicies, Pod Security Admission `restricted`, in-cluster TLS, image signing/scanning.

## Time breakdown

| Task | Time |
|------|------|
| App Dockerfile + minimal service | 45-60 min |
| Helm chart + dev/prod values | 90-120 min |
| Rollout strategy & rollback | 30-60 min |
| Observability / metrics stack | 90-120 min |
| Backup & restore docs | 20-30 min |
| README & hidden challenge explanation | 60-90 min |
| **Total** | **~6-8 h** |
