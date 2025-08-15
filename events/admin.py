from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
 list_display = ('title', 'event_type', 'start_date', 'end_date', 'capacity', 'registered_count', 'is_active')
 list_filter = ('event_type', 'is_active', 'start_date')
 search_fields = ('title', 'description')
 ordering = ('-start_date',)
 raw_id_fields = ('organizer',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
 list_display = ('user', 'event', 'registration_date', 'status')
 list_filter = ('status', 'registration_date', 'event__event_type')
 search_fields = ('user__username', 'event__title')
 ordering = ('-registration_date',)
 raw_id_fields = ('user', 'event')