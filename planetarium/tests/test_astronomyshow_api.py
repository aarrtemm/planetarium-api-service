import os
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowTheme, PlanetariumDome, ShowSession
from planetarium.serializers import AstronomyShowListSerializer, AstronomyShowDetailSerializer

SHOW_URL = reverse("planetarium:astronomyshow-list")
SHOW_SESSION_URL = reverse("planetarium:showsession-list")

def sample_show(**params):
    defaults = {
        "title": "Testtitle",
        "description": "TestDescription",
    }
    defaults.update(params)

    return AstronomyShow.objects.create(**defaults)


def sample_theme(**params):
    defaults = {
        "name": "TestTheme"
    }
    defaults.update(params)

    return ShowTheme.objects.create(**defaults)


def sample_planetarium_dome(**params):
    defaults = {
        "name": "testDome",
        "rows": 10,
        "seats": 10
    }
    defaults.update(params)

    return PlanetariumDome.objects.create(defaults)


def sample_show_session(**params):
    planetarium_dome = PlanetariumDome.objects.create(
        name="TestDome",
        rows=10,
        seats_in_row=10
    )
    defaults = {
        "astronomy_show": None,
        "planetarium_dome": planetarium_dome,
        "show_time": "2022-06-02 14:00:00",
    }

    defaults.update(params)

    return ShowSession.objects.create(**defaults)


def detail_url(show_id):
    return reverse("planetarium:astronomyshow-detail", args=[show_id])


def image_upload_url(show_id):
    return reverse("planetarium:astronomyshow-upload-image", args=[show_id])


class ShowImageUploadTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.theme = sample_theme()
        self.show = sample_show()
        self.show.themes.add(self.theme)
        self.show.save()
        self.show_session = sample_show_session(astronomy_show=self.show)

    def tearDown(self) -> None:
        self.show.image.delete()

    def test_upload_image_to_show(self):
        url = image_upload_url(self.show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.show.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.show.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.show.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_astronomy_show_list(self):
        url = SHOW_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                data={
                    "title": "TestTitle",
                    "description": "Description",
                    "themes": [1],
                    "image": ntf,
                      },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        show = AstronomyShow.objects.get(title="TestTitle")
        self.assertFalse(show.image)

    def test_image_url_is_shown_on_astronomy_show_detail(self):
        url = image_upload_url(self.show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(detail_url(self.show.id))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_astronomy_show_list(self):
        url = image_upload_url(self.show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(SHOW_URL)

        self.assertIn("image", res.data[0].keys())

    def test_image_url_is_shown_on_movie_session_detail(self):
        url = image_upload_url(self.show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(SHOW_SESSION_URL)

        self.assertIn("astronomy_show_image", res.data[0].keys())


class UnauthenticatedMovieApiTest(TestCase):
    def setUp(self) -> None:
        self.client =APIClient()

    def test_auth_required(self):

        res = self.client.get(SHOW_URL)
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMovieApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_astronomy_show(self):
        sample_show()
        show_with_theme = sample_show()

        theme = ShowTheme.objects.create(name="TestTheme")
        show_with_theme.themes.add(theme)

        response = self.client.get(SHOW_URL)
        shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(shows, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_filter_astronomy_show_by_themes(self):
        show1 = sample_show(title="Show 1")
        show2 = sample_show(title="Show 2")

        theme1 = ShowTheme.objects.create(name="testTheme1")
        theme2 = ShowTheme.objects.create(name="testTheme2")

        show1.themes.add(theme1)
        show2.themes.add(theme2)

        show3 = sample_show(title="Show without themes")

        response1 = self.client.get(
            SHOW_URL,
            {"themes": f"{theme1.id},{theme2.id}"}
        )

        serializer1 = AstronomyShowListSerializer(show1)
        serializer2 = AstronomyShowListSerializer(show2)
        serializer3 = AstronomyShowListSerializer(show3)

        self.assertIn(serializer1.data, response1.data)
        self.assertIn(serializer2.data, response1.data)
        self.assertNotIn(serializer3.data, response1.data)

    def test_show_retrieve(self):
        show = sample_show(title="ShowTest")
        url = detail_url(show.id)

        response = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(show)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer.data, response.data)

    def test_create_show_forbidden(self):
        payload = {
            "title": "MovieTest",
            "description": "TestDes",
        }

        response = self.client.post(SHOW_URL, payload)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_show_with_themes(self):
        theme = ShowTheme.objects.create(name="testTheme")
        payload = {
            "title": "MovieTest",
            "description": "TestDes",
            "themes": [theme.id, ]
        }
        response = self.client.post(SHOW_URL, payload)
        show = AstronomyShow.objects.get(id=response.data["id"])

        themes = show.themes.all()

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(themes.count(), 1)
        self.assertIn(theme, themes)

    def test_create_show_without_themes(self):
        payload = {
            "title": "MovieTest",
            "description": "TestDes",
        }

        response = self.client.post(SHOW_URL, payload)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_show(self):
        payload = {
            "title": "MovieTest2",
            "description": "testDesc"
        }

        theme = ShowTheme.objects.create(name="TestGenre")

        show = sample_show(title="ShowTest1")

        show.themes.add(theme)

        url = detail_url(show.id)

        response = self.client.patch(url, payload)

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

