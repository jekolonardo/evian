from django.contrib import admin

from .models import Course, CourseIndex, CourseIndexType, ClassTaker, ClassInstructor, Class, Attendance
# Register your models here.
admin.site.register(Course)
admin.site.register(CourseIndex)
admin.site.register(CourseIndexType)
admin.site.register(ClassTaker)
admin.site.register(ClassInstructor)
admin.site.register(Class)
admin.site.register(Attendance)