from django.urls import path
from . import views

urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/perks", views.ExperiencePerks.as_view()),
    path("<int:pk>/bookings", views.ExperienceBookings.as_view()),
    path(
        "<int:experience_pk>/bookings/<int:booking_pk>",
        views.ExperienceBookingsDetail.as_view(),
    ),
    path("perks/", views.Perks.as_view()),
    path("perks/<int:pk>", views.PerkDetail.as_view()),
]
