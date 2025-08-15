from rest_framework import serializers
from .models import Event, EventRegistration
from accounts.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    available_capacity = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    can_register = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'start_date', 'end_date',
                 'capacity', 'registered_count', 'available_capacity', 
                 'location', 'event_type', 'organizer', 'is_active',
                 'is_full', 'can_register', 'created_at')
        read_only_fields = ('registered_count', 'organizer')
    
    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)

class EventRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = ('id', 'user', 'event', 'registration_date', 'status')
        read_only_fields = ('user', 'registration_date')

class EventRegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ('event',)
    
    def validate_event(self, value):
        if not value.can_register():
            raise serializers.ValidationError("امکان ثبت‌نام در این رویداد وجود ندارد")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)