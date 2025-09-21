
from django.urls import path, include
from typing import List
from store.timepass.api.v1.generic.view import CurdGenericAPIView


urlpatterns: List = [
  path("hello/", CurdGenericAPIView.as_view() , name="hello")
]
 