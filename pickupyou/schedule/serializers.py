from rest_framework import serializers

from pickupyou.schedule.models import Driver, Coordinates, Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    end_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "title",
            "day",
            "start_time",
            "end_time",
            "driver",
            "pickup_point",
            "destination_point"
        ]


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Driver
        fields = ["id", "first_name", "last_name", "url", "orders"]


class CoordinatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coordinates
        fields = ["latitude", "longitude"]
