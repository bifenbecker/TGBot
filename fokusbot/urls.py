from django.contrib import admin
from django.urls import path

from users.views import UpdateBot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fokus-bot/retgefafsfwegbfbvf', UpdateBot.as_view()),
]
