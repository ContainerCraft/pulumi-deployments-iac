from pulumi_pulumiservice import TtlSchedule, DriftSchedule, DeploymentSchedule, PulumiOperation

def pulumi_schedule(
        organization_name: str,
        project_name: str,
        stack_name: str
    ):

    drift_schedule = DriftSchedule(
        f"{project_name}/{stack_name}-scheduled-drift",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        schedule_cron="0 0 * * 0",
        auto_remediate=False
    )

    preview_schedule = DeploymentSchedule(
        f"{project_name}/{stack_name}-scheduled-preview",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        timestamp="2026-01-01T00:00:00Z",
        pulumi_operation=PulumiOperation.PREVIEW
    )

    deploy_schedule = DeploymentSchedule(
        f"{project_name}/{stack_name}-scheduled-deploy",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        schedule_cron="0 0 * * 0",
        pulumi_operation=PulumiOperation.UPDATE
    )

    ttl_schedule = TtlSchedule(
        f"{project_name}/{stack_name}-scheduled-ttl",
        organization=organization_name,
        project=project_name,
        stack=stack_name,
        timestamp="2026-01-01T00:00:00Z",
        delete_after_destroy=False
    )

    return
