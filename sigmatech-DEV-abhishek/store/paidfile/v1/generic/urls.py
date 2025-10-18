from django.urls import path, include
from typing import List
from store.paidfile.v1.generic import views as generic_views

urlpatterns: List = [
    path('v1/paidfile/', generic_views.PaidfileListingGenericAPIView.as_view() , name='hello-world'),
]
