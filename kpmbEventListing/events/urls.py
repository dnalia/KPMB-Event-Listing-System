from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('index/', views.index, name='index'),
    path('student/register/', views.student_register, name='student_register'),
    path('student_login/', views.student_login, name='student_login'),
    path('student/<str:student_id>/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/<str:student_id>/search_events/', views.search_events_by_organizer, name='search_events_by_organizer'),
    path('student/<str:student_id>/event/<int:event_id>/add_feedback/', views.add_feedback, name='add_feedback'),
    path('student/<str:student_id>/event/<int:event_id>/confirm_join/', views.confirm_join_event, name='confirm_join_event'),
    path('student/<str:student_id>/event/<int:event_id>/update_feedback/', views.update_feedback, name='update_feedback'),
    path('student/<str:student_id>/event/<int:event_id>/feedback/', views.view_feedback, name='view_feedback'),
    path('student/<str:student_id>/event/<int:event_id>/feedback/delete/', views.delete_feedback, name='delete_feedback'),

    path('organizer/<str:organizer_id>/event/<int:event_id>/attendance/', views.view_attendance, name='view_attendance'),
    path('organizer_login/', views.organizer_login, name='organizer_login'),
    path('organizer_register/', views.organizer_register, name='organizer_register'),
    path('organizer/<str:organizer_id>/add_event/', views.add_event, name='add_event'),
    path('organizer/<str:organizer_id>/event_list/', views.event_list, name='event_list'), 
    path('organizer/<str:organizer_id>/update_event_date/<int:event_id>/', views.update_event_date, name='update_event_date'),
    path('organizer/<str:organizer_id>/confirm_delete_event/<int:event_id>/', views.confirm_delete_event, name='confirm_delete_event'),
]
