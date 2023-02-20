from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("<int:pk>/amenities", views.RoomPhotos.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
    # path("",views.see_all_rooms),
    # path("<int:room_id>/<str:room_name>",views.see_one_room),
    # path("<str:room_name>",views.s)
]
