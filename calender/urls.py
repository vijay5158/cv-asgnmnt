from django.urls import path, include,re_path
from rest_framework.routers import DefaultRouter

from .views import GoogleCalendarInitView,GoogleCalendarRedirectView



# router = DefaultRouter()
# router.register(r'v1/calendar/init/', GoogleCalendarInitView, basename='gc_init')
# router.register(r'v1/calendar/redirect/', GoogleCalendarRedirectView, basename='gc_redirect')

# # urlpatterns = router.urls

# urlpatterns = [
#     re_path(r'', include(router.urls)),
# ]

urlpatterns = [
    path('v1/calendar/init/', GoogleCalendarInitView, name='google_permission'),
    path('v1/calendar/redirect/', GoogleCalendarRedirectView, name='google_redirect')
]
