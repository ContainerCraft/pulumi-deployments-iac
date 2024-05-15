# Pulumi Cloud Deployments

- TTL Stacks
- Scheduled Deployments
- Drift Detection

## Getting Started

* requires Pulumi Cloud [Personal Access Token](https://www.pulumi.com/docs/pulumi-cloud/access-management/access-tokens/#creating-personal-access-tokens)

1. Add `PULUMI_ACCESS_TOKEN` secret to [Github Codespaces Secrets](https://github.com/settings/codespaces)
2. Add CIVO API Key secret to Pulumi stack Config or Pulumi ESC
3. Open repository in Github Codespaces
4. Login and create a new Pulumi stack

```bash
pulumi login
pulumi org set-default ContainerCraft
pulumi stack select --create dev
vim pulumi/stacks/Pulumi.dev.yaml
```

5. For Pulumi ESC, add your CIVO environment to `pulumi/stacks/Pulumi.dev.yaml`:

```yaml
environment:
  - civo
```

6. Configure deployment settings

> NOTE: First deploy with Pulumi Cloud DeploymentSettings disabled since our stack needs to be created before we can deploy Pulumi Cloud stack deployments configuration.

```bash
# Pulumi Project IaC specific settings

# Enable CIVO Infrastructure Deployment
pulumi config set civo_kubernetes.deploy true

# Enable Pulumi Cloud Stack Deployments Configuration
pulumi config set pulumicloud.deployment true

# Enable Pulumi Cloud Stack Deployments:
# - Pulumi Preview Deployments Schedule
pulumi config set pulumicloud.schedule true
```

7. Deploy the stack

```bash
pulumi preview
pulumi up
```

8. Destroy the stack

```bash
pulumi destroy --refresh=true --skip-preview -y
pulumi stack rm dev
```

---

## Tips

```bash
# Load the kubeconfig locally for kubectl cli usage
mkdir ~/.kube && pulumi stack output kubeconfig --show-secrets > ~/.kube/config

# Try a kubectl command like this to list all pods
kubectl get po -A
```
