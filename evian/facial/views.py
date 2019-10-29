import json
import base64
import datetime
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from login.models import User
from course.models import Course, CourseIndex, CourseIndexType, Class, Attendance
from django.conf import settings
from face_recognition import api
import numpy as np

# Create your views here.


class FacialView(View):
    def updateAttendance(self, matric, sign=""):
        student = User.objects.get(matric_no = matric)
        course = Course.objects.get(course_code = "CZ3002")
        course_index = CourseIndex.objects.get(index = "12345")
        course_index_type = CourseIndexType.objects.get(course_index = course_index, class_type="lab")
        today = datetime.datetime.now()

        tdelta = (3 - datetime.datetime.today().weekday()) % 7
        today_date = today.date() + datetime.timedelta(days=tdelta)
        # today_date = today.date()
        
        time = course_index_type.time
        today_time = today.time()
        class_session = Class.objects.get(course_index_type = course_index_type, datetime__date = today_date)
        attendance = Attendance.objects.get(class_session = class_session, student = student)
        print(attendance)
        attendance.status = "present"
        attendance.attendance_time = today_time
        attendance.signature = sign
        attendance.save()

    def getAttendanceData(self):
         # student = User.objects.get(matric_no = "U1620133D")
        course = Course.objects.get(course_code = "CZ3002")
        course_index = CourseIndex.objects.get(index = "12345")
        course_index_type = CourseIndexType.objects.get(course_index = course_index, class_type="lab")
        today = datetime.datetime.now()

        tdelta = (3 - datetime.datetime.today().weekday()) % 7
        today_date = today.date() + datetime.timedelta(days=tdelta)
        # today_date = today.date()
        
        time = course_index_type.time
        today_time = today.time()
        class_session = Class.objects.get(course_index_type = course_index_type, datetime__date = today_date)
        attendance = Attendance.objects.filter(class_session = class_session)

        student_list = []
        for a in attendance:
            student_list.append(a.student)
        
        pic_list = []
        for s in student_list:
            pic_list.append(s.face_image)

        p_encs = []
        for p in pic_list:
            p_dir = settings.MEDIA_ROOT+"/"+str(p)
            p_image = api.load_image_file(p_dir)
            p_enc = api.face_encodings(p_image)[0]
            p_encs.append(p_enc)

        return student_list, pic_list, p_encs

    def post(self, request):
        body = json.loads(request.body)
        count = body.get('count')
        print (count)

        # print(image)
        # print(type(image))

        if count == 1 or count == 2 or count == 3:

            image = body.get('image')
            # print(image)
            try:
                image = image[23:]
            except:
                data = {'state': 'error', 'info':'error-image',
                'message': 'Image Upload Error! Please try again.', 'mode': 'img'}
                return JsonResponse(data)
            print (type(image))

            # print(image)

            # Get Image and store in unknown.jpg
            try:
                imgdata = BytesIO(base64.b64decode(image))
            except:
                data = {'state': 'error', 'info':'error-image',
                'message': 'Image Upload Error! Please try again.', 'mode': 'img'}
                return JsonResponse(data)
            print(type(imgdata))
            # filename = 'unknown.jpg'  # I assume you have a way of picking unique filenames

            # with open(filename, 'wb') as f:
            #     f.write(base64.b64decode(image))

            # Get list of students, and list of face encodings
            student_list, pic_list, p_encs = self.getAttendanceData()
            # print (p_encs)
            # Get encoding of captured image
            try:
                unknown = api.load_image_file(imgdata)
            except:
                data = {'state': 'error', 'info':'error-image',
                'message': 'Image Upload Error! Please try again.', 'mode': 'img'}
                return JsonResponse(data)
            unknown_enc = api.face_encodings(unknown)

            if (len(unknown_enc) == 1):
                unknown_enc = unknown_enc[0]
                face_distance = api.face_distance(p_encs, unknown_enc)
                face_distance = face_distance.tolist()
                print(face_distance)
            elif (len(unknown_enc) > 1):
                data = {'state': 'error',
                    'message': 'Authentication failed! Multiple faces detected', 'mode': 'img'}
                return JsonResponse(data)
            else:
                data = {'state': 'error',
                    'message': 'Authentication failed! No face detected', 'mode': 'img'}
                return JsonResponse(data)

            # Face recognition with tolerance of 0.5
            lt5 = {}
            cnt_lt5 = 0
            for f in face_distance:
                if f <= 0.5:  # Edit value here
                    lt5[student_list[face_distance.index(f)].matric_no] = 1
                    cnt_lt5 += 1
                else:
                    lt5[student_list[face_distance.index(f)].matric_no] = 0

            print(lt5)
            print(cnt_lt5)

            if (cnt_lt5 == 1):
                matric_no = list(lt5.keys())[list(lt5.values()).index(1)]
                message = matric_no + " Authentication success!"
                data = {'state': 'success', 'info': 'lt5',
                    'message': message, 'mode': 'img'}
                self.updateAttendance(matric_no)
                return JsonResponse(data)
            elif (cnt_lt5 > 1):
                s = []
                for matric, state in lt5.items():
                    if state == 1:
                        s.append(matric)

                data = {'state': 'warning', 'info': 'lt5',
                    'message': 'Multiple students recognized', 'mode': 'img', 'students':s}
                return JsonResponse(data)
            else:
                data = {'state': 'error',
                'message': 'Authentication failed!', 'mode': 'img'}
                return JsonResponse(data)

            # print(attendance)
            # attendance.status = "present"
            # attendance.attendance_time = today_time
            # attendance.save()

        elif count == 4:

            image = body.get('image')
            # print (image)
            try:
                image = image[23:]
            except:
                data = {'state': 'error', 'info':'error-image',
                'message': 'Image Upload Error! Please try again.', 'mode': 'img'}
                return JsonResponse(data)
            print (type(image))

            # Get Image and store in unknown.jpg
            try:
                imgdata = BytesIO(base64.b64decode(image))
            except:
                data = {'state': 'error', 'info':'error-image',
                'message': 'Image Upload Error! Please try again.', 'mode': 'img'}
                return JsonResponse(data)

            print(type(imgdata))
            # filename = 'unknown.jpg'  # I assume you have a way of picking unique filenames

            # with open(filename, 'wb') as f:
            #     f.write(imgdata)

            # Get list of students, and list of face encodings
            student_list, pic_list, p_encs = self.getAttendanceData()
            # print (p_encs)
            # Get encoding of captured image
            try:
                unknown = api.load_image_file(imgdata)
            except:
                data = {'state': 'error', 'info':'error-image',
                'message': 'Image Upload Error! Please try again.', 'mode': 'img'}
                return JsonResponse(data)
            unknown_enc = api.face_encodings(unknown)

            if (len(unknown_enc) == 1):
                unknown_enc = unknown_enc[0]
                face_distance = api.face_distance(p_encs, unknown_enc)
                face_distance = face_distance.tolist()
                print(face_distance)
            elif (len(unknown_enc) > 1):
                data = {'state': 'error',
                    'message': 'Authentication failed! Multiple faces detected', 'mode': 'img'}
                return JsonResponse(data)
            else:
                data = {'state': 'error',
                    'message': 'Authentication failed! No face detected', 'mode': 'img'}
                return JsonResponse(data)

            # Face recognition with tolerance of 0.6
            lt6 = {}
            cnt_lt6 = 0
            for f in face_distance:
                if f <= 0.6:
                    lt6[student_list[face_distance.index(f)].matric_no] = 1
                    cnt_lt6 += 1
                else:
                    lt6[student_list[face_distance.index(f)].matric_no] = 0

            print(lt6)
            print(cnt_lt6)

            if (cnt_lt6 == 1):
                matric_no = list(lt6.keys())[list(lt6.values()).index(1)]
                message = matric_no + " detected. Please sign"
                data = {'state': 'success', 'info': 'lt6',
                    'message': message, 'mode': 'sign', 'matric':matric_no}
                return JsonResponse(data)
            elif (cnt_lt6 > 1):
                s = []
                for matric, state in lt6.items():
                    if state == 1:
                        s.append(matric)

                data = {'state': 'warning', 'info': 'lt6',
                    'message': 'Multiple students recognized', 'mode': 'img', 'students':s}
                return JsonResponse(data)
            else:
                data = {'state': 'error',
                'message': 'Authentication failed!', 'mode': 'img'}
                return JsonResponse(data)


        elif count == 5:
            
            matric = body.get('matric')
            if (not matric):
                data = {'state': 'error', 'info':'error-matric',
                'message': 'Matric not provided!', 'mode': 'img'}
                return JsonResponse(data)
            message = matric + " detected. Please sign"
            print(matric)
            data = {'state': 'info',
                    'message': message, 'mode': 'sign', 'matric':matric}
        elif count == 6:
            
            matric = body.get('matric')
            if (not matric):
                data = {'state': 'error', 'info':'error-matric',
                'message': 'Matric not provided!', 'mode': 'img'}
                return JsonResponse(data)

            message = matric + " Authentication success!"
            print(matric)
            data = {'state': 'success',
                    'message': message, 'mode': 'img'}

            image = body.get('image')
            
            image = image[22:]
            if (not image):
                data = {'state': 'error', 'info':'error-image',
                'message': 'Image Upload Error! Please try again.', 'mode': 'img'}
                return JsonResponse(data)

            # imgdata = base64.b64decode(image)
            print (type(image))
            self.updateAttendance(matric, image)
        else:
            data = {'state': 'error', 'info': 'error-count',
                    'message': "Invalid State", 'mode': 'img'}

        return JsonResponse(data)
