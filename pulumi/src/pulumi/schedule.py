from pulumi_pulumiservice import TtlSchedule, DriftSchedule, DeploymentSchedule, PulumiOperation

def pulumi_schedule(
        organization_name: str,
        project_name: str,
        stack_name: str
    ):

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/schedules
    deploy_schedule = DeploymentSchedule(
        f"{project_name}/{stack_name}-scheduled-deploy",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        schedule_cron="0 0 * * 0", # Deploy/Update Sunday at midnight UTC
        pulumi_operation=PulumiOperation.UPDATE
    )

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/drift
    drift_schedule = DriftSchedule(
        f"{project_name}/{stack_name}-scheduled-drift",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        schedule_cron="0 8 * * *", # Pulumi preview every day at 08:00 UTC
        auto_remediate=False
    )

    preview_schedule = DeploymentSchedule(
        f"{project_name}/{stack_name}-scheduled-preview",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        timestamp="2024-05-17T00:00:00Z", # Preview stack on May 17, 2024 at midnight UTC
        pulumi_operation=PulumiOperation.PREVIEW
    )

    # https://www.pulumi.com/docs/pulumi-cloud/deployments/ttl
    ttl_schedule = TtlSchedule(
        f"{project_name}/{stack_name}-scheduled-ttl",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        timestamp="2024-05-18T00:00:00Z", # Destroy stack on May 18, 2024 at midnight UTC
        delete_after_destroy=False
    )

    # return pulumi schedules as a single tuple
    return (deploy_schedule, drift_schedule, preview_schedule, ttl_schedule)
