from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from planetarium.permissions import IsAdminOrAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ReservationSerializer,
    ShowSessionDetailSerializer, ReservationListSerializer, ShowSessionListSerializer, AstronomyShowListSerializer,
)


class DefaultPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class ShowThemeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    pagination_class = DefaultPagination
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly, )


class AstronomyShowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = AstronomyShow.objects.all().prefetch_related(
        "themes"
    )
    serializer_class = AstronomyShowSerializer
    pagination_class = DefaultPagination
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        return AstronomyShowSerializer

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset
        themes = self.request.query_params.get("themes")

        if themes:
            themes_ids = self._params_to_ints(themes)
            queryset = queryset.filter(themes__id__in=themes_ids)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "themes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filtering by themes (ex. ?themes=1,2)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PlanetariumDomeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    pagination_class = DefaultPagination
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)


class ShowSessionPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 100


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        ShowSession.objects.all()
        .annotate(
            tickets_available=(
                F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer
    pagination_class = ShowSessionPagination
    permission_classes = (IsAdminOrAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionDetailSerializer
        return ShowSessionSerializer

    def get_queryset(self):
        """Retrieve the movies with filters"""
        queryset = self.queryset
        date = self.request.query_params.get("date")
        title = self.request.query_params.get("title")

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if title:
            queryset = queryset.filter(astronomy_show__title__icontains=title)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description="Filtering by date (ex. ?date=2012-12-12)"
            ),
            OpenApiParameter(
                "title",
                type=str,
                description="Filtering by title (ex. ?title=Sun)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 100


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).prefetch_related(
            "tickets__show_session",
            "tickets__show_session__astronomy_show",
            "tickets__show_session__planetarium_dome"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
