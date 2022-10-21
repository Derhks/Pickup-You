import datetime
import math

import requests
from rest_framework import generics, permissions, viewsets

from pickupyou import settings
from pickupyou.schedule.serializers import (
    CoordinatesSerializer, DriverSerializer, OrderSerializer
)
from pickupyou.schedule.models import Coordinates, Driver, Order


class CoordinatesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows coordinates to be viewed or edited.
    """
    queryset = Coordinates.objects.all().order_by("id")
    serializer_class = CoordinatesSerializer
    permission_classes = [permissions.IsAuthenticated]


class DriverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows drivers to be viewed or edited.
    """
    queryset = Driver.objects.all().order_by("id")
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]


class DriverOrdersDetail(generics.ListAPIView):
    """
    API endpoint that allows to view the orders assigned to the driver on the
    specified day. Orders are sorted by pickup time.
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        This view should return a list of all orders for a driver on the given
        day.
        """
        day = self.kwargs["day"]
        pk = self.kwargs["pk"]
        queryset = Driver.objects.all().order_by("id")

        if day is not None:
            queryset = (
                queryset.filter(id=pk).first().
                orders.all().filter(day=day).order_by("start_time")
            )

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all().order_by("start_time")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetail(generics.ListAPIView):
    """
    API endpoint that allows you to view the orders assigned on the specified
    day.
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        This view should return a list of all the orders for the given day.
        """
        day = self.kwargs["day"]
        queryset = Order.objects.all().order_by("start_time")

        if day is not None:
            queryset = queryset.filter(day=day)

        return queryset


class NearestDriverDetail(generics.ListAPIView):
    """
    API endpoint that allows you to see the nearest driver.
    """
    serializer_class = DriverSerializer
    pagination_class = None

    def get_queryset(self):
        """
        This view should return the nearest driver.
        """
        query_params = self.request.GET
        day = query_params.get("day")
        hour = query_params.get("hour")
        latitude = int(query_params.get("latitude"))
        longitude = int(query_params.get("longitude"))

        if latitude < 0 or longitude < 0:
            raise ValueError

        drivers_location = self.get_active_drivers(day, hour)
        driver = self.get_nearest_driver(latitude, longitude, drivers_location)

        return driver

    def get_active_drivers(self, day: str, hour: str) -> list:
        """
        Obtains the active and available drivers on the indicated day and time.

        Args:
            day: str
                Order day
            hour:
                Order hour

        Returns:
            Driver list
        """
        url = settings.URL_DRIVERS_LOCATIONS
        response = requests.get(url)
        drivers_list: list[dict] = response.json().get("alfreds")
        drivers_location_list: list[dict] = []

        for driver in drivers_list:
            if day and hour in driver.get('lastUpdate'):
                drivers_location_list.append(driver)

        drivers_available = self.get_drivers_available(
            drivers_location_list, day, hour
        )

        drivers_location_available_list = [
            driver_location
            for driver_location in drivers_list
            if driver_location['id'] in drivers_available
        ]

        return drivers_location_available_list

    def get_drivers_available(
        self,
        drivers_location: list[dict],
        day: str,
        hour: str
    ) -> list[int]:
        """
        Gets the available drivers, i.e. those that do not have an active order.

        Args:
            drivers_location: list[dict]
                List of active driver's
            day: str
                Order day
            hour:
                Order hour

        Returns:
            List of available drivers
        """
        drivers_ids = []
        drivers_available_ids = []

        for driver in drivers_location:
            drivers_ids.append(driver.get("id"))

        drivers = Driver.objects.all().filter(id__in=drivers_ids).order_by("id")

        for driver in drivers:
            has_an_order = self.driver_has_an_active_order(driver, day, hour)

            if not has_an_order:
                drivers_available_ids.append(driver.id)

        return drivers_available_ids

    @staticmethod
    def driver_has_an_active_order(
        driver: DriverSerializer,
        day: str,
        hour: str
    ):
        """
        Checks if the driver has an active order at the specified time and on
        the specified day.

        Args:
            driver: DriverSerializer
                Object DriverSerializer
            day: str
                Order day
            hour: str
                Order hour

        Returns:
            True if the driver has an active order, False otherwise
        """
        orders = driver.orders.all().filter(day=day)
        has_an_active_order = False

        for order in orders:
            start_time = order.start_time
            end_time = order.end_time
            hour = datetime.datetime.strptime(hour, '%H:%M:%S').time()

            if start_time <= hour <= end_time:
                has_an_active_order = True

        return has_an_active_order

    def get_nearest_driver(
        self,
        latitude: int,
        longitude: int,
        drivers_list: list
    ) -> DriverSerializer:
        """
        Gets the driver closest to the indicated point.

        Args:
            latitude: int
                Latitude of pick-up point
            longitude: int
                Longitude of the pick-up point
            drivers_list: list
                List with the location of the drivers

        Returns:
            The nearest driver
        """
        distances_list: list[dict] = []

        for driver in drivers_list:
            distances_list.append(
                self.get_distance(latitude, longitude, driver)
            )

        distances_list_sorted = (
            sorted(distances_list, key=lambda i: i["distance"])
        )

        if not distances_list_sorted:
            driver = None
        else:
            driver = (
                Driver.objects.all().filter(
                    id=distances_list_sorted[0].get("id")
                )
            )

        return driver

    @staticmethod
    def get_distance(latitude: int, longitude: int, driver: dict) -> dict:
        """
        Gets the distance between the driver and the given point.

        Args:
            latitude: int
                Latitude of pick-up point
            longitude: int
                Longitude of the pick-up point
            driver: dict
                Driver location

        Returns:
            A dict with the distance from the driver to the given point
        """
        distance = math.sqrt(
            (int(driver.get("lat")) - latitude)**2 +
            (int(driver.get("lng")) - longitude)**2
        )

        return {
            "id": driver.get("id"),
            "distance": distance
        }
