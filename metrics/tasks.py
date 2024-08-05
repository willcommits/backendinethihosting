from celery import shared_task
from celery.utils.log import get_task_logger

from monitoring.models import Node
from .models import UptimeMetric, RTTMetric
from .ping import ping

logger = get_task_logger(__name__)


@shared_task
def run_pings():
    for device in Node.objects.filter(ip__isnull=False):
        ping_data = ping(device.ip)
        rtt_data = ping_data.pop("rtt", None)
        UptimeMetric.objects.create(mac=device.mac, **ping_data)
        if rtt_data:
            RTTMetric.objects.create(mac=device.mac, **rtt_data)
        logger.info(f"PING {device.ip}")
