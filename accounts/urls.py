from django.urls import path
from .views import (
    login_view,
    dashboard,
    manage_users,
    assign_investigators,
    system_reports,
    logout_view,
    signup_view,
     investigator_dashboard,
    update_case_status,
    analyze_case,assigned_cases,analyst_case_stats,analyst_reports,view_case_info
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('manage-users/', manage_users, name='manage_users'),
    path('reports/', system_reports, name='system_reports'),
    path('analyst/stats/', analyst_case_stats, name='case_stats'),
    path('assign-investigators/', assign_investigators, name='assign_investigators'),
    path('investigator/', investigator_dashboard, name='investigator_dashboard'),
    path('case/<int:case_id>/status/', update_case_status, name='update_case_status'),
    path('analyst/cases/', assigned_cases, name='assigned_cases'),
    path('analyst/analyze/<int:case_id>/', analyze_case, name='analyze_case'),
    path('analyst/reports/', analyst_reports, name='analyst_reports'),
    path('analyst/case/<int:case_id>/view/', view_case_info, name='view_case_info'),
]
