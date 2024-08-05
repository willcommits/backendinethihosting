from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from . import models


class UptimeMetricSerializer(ModelSerializer):
    """Serializes UptimeMetric objects from django model to JSON."""

    node = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """UptimeMetricSerializer metadata."""

        model = models.UptimeMetric
        fields = "__all__"


class FailuresMetricSerializer(ModelSerializer):
    """Serializes FailuresMetric objects from django model to JSON."""

    class Meta:
        """FailuresMetricSerializer metadata."""

        model = models.FailuresMetric
        fields = "__all__"


class ResourcesMetricSerializer(ModelSerializer):
    """Serializes ResourcesMetric objects from django model to JSON."""

    class Meta:
        """ResourcesMetricSerializer metadata."""

        model = models.ResourcesMetric
        fields = "__all__"


class RTTMetricSerializer(ModelSerializer):
    """Serializes RTTMetric objects from django model to JSON."""

    class Meta:
        """RTTMetricSerializer metadata."""

        model = models.RTTMetric
        fields = "__all__"


class DataUsageMetricSerializer(ModelSerializer):
    """Serializes DataUsageMetric objects from django model to JSON."""

    class Meta:
        """DataUsageMetricSerializer metadata."""

        model = models.DataUsageMetric
        fields = "__all__"
