"""evian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from facial.views import FacialView
from login.views import LoginView
from course.views import AttendanceView, CourseStatsView, SessionAttendanceView, OverwriteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('facial/', FacialView.as_view()),
    path('login/', LoginView.as_view()),
    path('attendance/', AttendanceView.as_view()), 
    path('course-stats/', CourseStatsView.as_view()),
    path('session-attendance/', SessionAttendanceView.as_view()),
    path('overwrite/', OverwriteView.as_view()),
]
