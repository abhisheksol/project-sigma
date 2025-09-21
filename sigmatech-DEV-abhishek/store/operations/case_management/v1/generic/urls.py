
from django.urls import path, include
from typing import List
from store.operations.case_management.v1.generic.views import CaseManagementListGenericView


urlpatterns: List = [
  path("list/", CaseManagementListGenericView.as_view() , name="")
]
 