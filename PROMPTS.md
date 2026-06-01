# LLM Usage

Most of this project was written by hand. I used Claude Code (an agentic assistant in the repo) 
narrowly - mainly to debug image delivery, sort out the monitoring CRD bootstrap, split the charts, and draft docs. 
The prompts below cover the main ones; design, code, and verification are mine.

## Prompts by area

### Cluster & image delivery
- minikube from scratch (3 nodes, calico, taint)
- how is the image delivered into the cluster? it must work from the cluster
- image not picked up after a rebuild

### Monitoring
- chart complains about missing CRDs; install them by command, not manual copy
- delete the CRDs, test the upgrade-job option
- CRD error when switching to standalone
- how to add a minimal standalone Prometheus

### Charts & namespaces
- one chart is spaghetti - split monitoring and vault into separate charts
- delete the old stack/release, deploy the new ones
- everything is in default - split across namespaces

### Docs
- README, OPERATIONS
