from django.urls import path, include
from typing import List
from store.operations.referal_files.v1 import views as referal_views

urlpatterns: List = [
    # path("case-management/", include("store.operations.case_management.urls")),
    path("referral-file-listing/", referal_views.referral_file_listing, name="referral-file-listing"),
   
   
]
