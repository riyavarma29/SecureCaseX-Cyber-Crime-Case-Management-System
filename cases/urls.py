from django.urls import path
from .views import case_list, create_case, update_case_status
from . import views
urlpatterns = [
    path('', views.case_list, name='case_list'),
    path('create/', views.create_case, name='create_case'),
    path('<int:pk>/', views.case_detail, name='case_detail'),
    path('<int:case_id>/status/', views.update_case_status, name='update_case_status'),
    path('<int:pk>/assign/', views.assign_investigator, name='assign_investigator'),
    path('assign-analyst/<int:case_id>/', views.assign_analyst, name='assign_analyst'),
]
