import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient

from pickupyou.schedule.models import Driver, Coordinates, Order


def get_driver() -> Driver:
    return Driver.objects.create(first_name="Julián", last_name="Sandoval")


class TestOrdersView(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username="test-user", password="12345")

    def test_get_orders_assigned_today(self):
        client = RequestsClient()
        client.auth = HTTPBasicAuth("test-user", "12345")
        response = client.get("http://localhost/orders/")

        got = response.status_code
        want = 200

        self.assertEqual(got, want)


class TestDriverOrdersDetail(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username="test-user", password="12345")
        get_driver()

    def test_get_orders_assigned_to_the_driver(self):
        client = RequestsClient()
        client.auth = HTTPBasicAuth("test-user", "12345")
        response = client.get("http://localhost/drivers/1/orders/2022-10-19/")

        got = response.status_code
        want = 200

        self.assertEqual(got, want)


class TestOrdersDetail(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username="test-user", password="12345")

    def test_get_the_assigned_orders_on_the_indicated_day(self):
        client = RequestsClient()
        client.auth = HTTPBasicAuth("test-user", "12345")
        response = client.get("http://localhost/orders/2022-10-19/")

        got = response.status_code
        want = 200

        self.assertEqual(got, want)


class TestNearestDriverDetail(TestCase):
    nearest_driver_url = (
        "http://localhost/nearest-driver/"
        "?latitude=1&longitude=7&day=2021-12-10&hour=00:00:00"
    )

    def setUp(self) -> None:
        User.objects.create_user(username="test-user", password="12345")

    def test_get_nearest_driver_none(self):
        client = RequestsClient()
        client.auth = HTTPBasicAuth("test-user", "12345")
        response = client.get(self.nearest_driver_url)

        got = response.status_code
        want = 200

        self.assertEqual(got, want)

    def test_get_nearest_driver_without_order(self):
        get_driver()
        client = RequestsClient()
        client.auth = HTTPBasicAuth("test-user", "12345")
        response = client.get(self.nearest_driver_url)

        got = response.status_code
        want = 200

        self.assertEqual(got, want)

    def test_get_nearest_driver(self):
        pickup_point = Coordinates.objects.create(latitude=5, longitude=9)
        destination_point = Coordinates.objects.create(latitude=2, longitude=6)
        Order.objects.create(
            title="Test",
            day="2021-12-10",
            start_time=datetime.time(0, 0),
            driver=get_driver(),
            pickup_point=pickup_point,
            destination_point=destination_point
        )
        client = RequestsClient()
        client.auth = HTTPBasicAuth("test-user", "12345")
        response = client.get(self.nearest_driver_url)

        got = response.status_code
        want = 200

        self.assertEqual(got, want)
