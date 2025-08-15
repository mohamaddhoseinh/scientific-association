from django.urls import path
from .views import (
 EventListCreateView, EventDetailView,
 EventRegisterView, EventCancelRegistrationView,
 MyEventRegistrationsView
)

app_name = 'events'

urlpatterns = [
 path('', EventListCreateView.as_view(), name='event_list'),
 path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
 path('<int:pk>/register/', EventRegisterView.as_view(), name='event_register'),
 path('<int:pk>/cancel/', EventCancelRegistrationView.as_view(), name='event_cancel'),
 path('my-registrations/', MyEventRegistrationsView.as_view(), name='my_registrations'),
]