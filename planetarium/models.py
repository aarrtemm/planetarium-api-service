from django.conf import settings
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=63)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow, on_delete=models.CASCADE, related_name="shows"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome, on_delete=models.CASCADE, related_name="shows"
    )
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
