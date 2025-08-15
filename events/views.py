from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from .models import Event, EventRegistration
from .serializers import (
    EventSerializer, EventRegistrationSerializer,
    EventRegistrationCreateSerializer
)

class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Event.objects.all()
        
        # فیلتر براساس query parameters
        event_type = self.request.query_params.get('type', None)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # فقط رویدادهای فعال و آینده
        if not self.request.user.is_authenticated or not self.request.user.is_admin():
            queryset = queryset.filter(
                is_active=True,
                start_date__gt=timezone.now()
            )
        
        return queryset.order_by('start_date')
    
    def perform_create(self, serializer):
        if not self.request.user.is_member():
            raise permissions.PermissionDenied("فقط اعضای انجمن می‌توانند رویداد ایجاد کنند")
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user and not request.user.is_admin():
            return Response(
                {"detail": "شما اجازه ویرایش این رویداد را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user and not request.user.is_admin():
            return Response(
                {"detail": "شما اجازه حذف این رویداد را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

class EventRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"detail": "رویداد یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # بررسی امکان ثبت‌نام
        if not event.can_register():
            return Response(
                {"detail": "امکان ثبت‌نام در این رویداد وجود ندارد"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # بررسی ثبت‌نام قبلی
        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            return Response(
                {"detail": "شما قبلاً در این رویداد ثبت‌نام کرده‌اید"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ثبت‌نام
        registration = EventRegistration.objects.create(
            user=request.user,
            event=event
        )
        
        # افزایش تعداد ثبت‌نام شدگان
        event.registered_count += 1
        event.save()
        
        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EventCancelRegistrationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            registration = EventRegistration.objects.get(
                user=request.user,
                event__pk=pk,
                status='registered'
            )
        except EventRegistration.DoesNotExist:
            return Response(
                {"detail": "ثبت‌نام یافت نشد"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # لغو ثبت‌نام
        registration.status = 'cancelled'
        registration.save()
        
        # کاهش تعداد ثبت‌نام شدگان
        event = registration.event
        event.registered_count -= 1
        event.save()
        
        return Response(
            {"detail": "ثبت‌نام با موفقیت لغو شد"},
            status=status.HTTP_200_OK
        )

class MyEventRegistrationsView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EventRegistration.objects.filter(
            user=self.request.user
        ).order_by('-registration_date')