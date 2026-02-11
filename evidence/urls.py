from django.urls import path
from .views import upload_evidence,view_case_evidence,generate_case_report

urlpatterns = [
    path('upload/<int:case_id>/', upload_evidence, name='upload_evidence'),
    path('case/<int:case_id>/evidence/', view_case_evidence, name='view_case_evidence'),
    path('analyst/case/<int:case_id>/report/', generate_case_report, name='generate_case_report'),

]
