from django.conf import settings
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()

    def __str__(self):
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow, on_delete=models.CASCADE, related_name="shows"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome, on_delete=models.CASCADE, related_name="shows"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return (f"Astronomy Show: {self.astronomy_show} | "
                f"Show time: {self.show_time}")


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user} | {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession, on_delete=models.CASCADE, related_name="ticket"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="ticket"
    )

    def __str__(self):
        return f"{self.show_session} | Row: {self.row} | Seat: {self.seat}"
