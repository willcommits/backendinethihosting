from celery import shared_task
from celery.utils.log import get_task_logger

from .sync.radiusdesk import run as syncrd
from .sync.unifi import run as syncunifi
from .checks import CheckStatus
from .models import Node, Alert

logger = get_task_logger(__name__)


@shared_task
def run_syncrd() -> None:
    """Celery task to sync the Django database with radiusdesk's mysql db."""
    logger.info("Syncing with radiusdesk")
    syncrd()


@shared_task
def run_syncunifi() -> None:
    """Celery task to sync the Django database with unifi's mongodb."""
    logger.info("Syncing with unifi")
    syncunifi()


@shared_task
def generate_alerts() -> None:
    """Celery task to monitor for alerts, generates them if necessary."""
    logger.info("Generating alerts")
    for n in Node.objects.all():
        current_status = n.check_results.status()
        current_status_level = current_status.alert_level()
        unresolved_alerts = Alert.objects.filter(node=n, resolved=False)
        # Only generate a new alert if the current state is worse than
        # that of an alert triggered last (or there are no previous alerts).
        # Otherwise we would be generating new alerts for the same state,
        # e.g. generating a WARNING alert for a node that has already got an
        # unresolved WARNING.
        if current_status != CheckStatus.OK:
            latest_alert = unresolved_alerts.order_by("-created").first()
            if not latest_alert or current_status_level > latest_alert.level:
                # Generate the alert
                alert = Alert.from_status(n, current_status)
                alert.save()
                logger.info("Generated an alert for %s: %s", n, alert)
        # Mark all previous alerts that were worse than the current status as resolved.
        # E.g. if a node generated a CRITICAL alert, but is now OK, that previous alert
        # is assumed to have been resolved.
        alerts_worse_than_current_status = unresolved_alerts.filter(level__gt=current_status_level)
        alerts_worse_than_current_status.update(resolved=True)
