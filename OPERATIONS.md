# Operations

Deploy, rollback and monitoring commands are in the README.

## Backup & restore
- app - stateless, nothing to back up
- helm release state - in Secrets `sh.helm.release.v1.*`; `helm get manifest|values <rel> -n <ns>` reproduces it
- Prometheus data - `emptyDir`, ephemeral by design
- Vault (dev) - in-memory; secret/auth re-seeded by the bootstrap job on `helm upgrade vault` (prod: persistent + `vault operator raft snapshot`)

## Troubleshooting
- `ErrImageNeverPull` - image is not on the node, run `app/build.sh`, push to cluster acceptable registry
- `/healthz` response is empty after a Vault restart - dev Vault is ephemeral, `helm upgrade vault` re-seeds
- pod stuck `Pending` in prod - check taint/toleration keys
