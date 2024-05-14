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
pulumi stack select --create dev
pulumi config set civo_kubernetes.deploy true
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
pulumi config set civo_kubernetes.deploy true
pulumi config set pulumi_cloud.deployment false
```

7. Deploy the stack

```bash
pulumi preview
pulumi up
```

8. Enable Pulumi Cloud deployments & re-deploy

```bash
pulumi config set pulumi_cloud.deployment true
pulumi preview
pulumi up
```

9. Destroy the stack

```bash
pulumi config set pulumi_cloud.deployment false
pulumi down
pulumi stack rm dev
```
