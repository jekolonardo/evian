import json
import base64
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.conf import settings
from .models import User, UserLogin
from course.models import Course, CourseIndex, ClassTaker, ClassInstructor

# Create your views here.
class LoginView(View):
    def post(self, request):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')

        print(username,password)
        try:
            user = UserLogin.objects.get(username=username, password=password)
        except UserLogin.DoesNotExist:
            user = None
        domain = None
        state = False
        encoded_string = ""
        course_list = []
        if (user):
            state = True

            user = user.user
            face_dir = settings.MEDIA_ROOT+"\\"+str(user.face_image)
            with open(face_dir, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            encoded_string = encoded_string.decode("utf-8")

            domain = user.domain

            matric_no = user.matric_no
            if (domain == "student"):
                classes = ClassTaker.objects.filter(student=user)
            elif (domain == "staff"):
                classes = ClassInstructor.objects.filter(staff=user)
            for c in classes:
                course_index = c.course_index
                course = course_index.course
                course_code = course.course_code
                course_name = course.course_name
                group = course_index.group
                course_list.append({
                    'code':course_code,
                    'name':course_name,
                    'group':group
                    })

        data = {'state':state,
        'domain':domain,
        'image':encoded_string,
        'course':course_list}

        print (data)
        return JsonResponse(data)
