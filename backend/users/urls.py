from django.urls import path

from .views import (
    FollowView,
    FollowListView,
)

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', FollowListView.as_view(),
         name='subscription'),
]