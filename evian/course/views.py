import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.duration import _get_duration_components
from login.models import User, UserLogin
from .models import Course, CourseIndex, CourseIndexType, ClassTaker, ClassInstructor, Attendance, Class
import datetime

# Create your views here.
class AttendanceView(View):
    def post(self, request):
        body = json.loads(request.body)
        username = body.get('username')
        domain = body.get('domain')
        course = body.get('course')

        print(username,domain,course)
        try:
            user = UserLogin.objects.get(username=username)
            user = user.user
        except UserLogin.DoesNotExist:
            user = None

        state = False
        data_list = []
        
        if (user and domain == "student" and domain == user.domain):
            state = True

            class_taker_list = ClassTaker.objects.filter(student=user)
            
            course_index_list = []
            for c in class_taker_list:
            	course_index = c.course_index
            	if (course_index.course.course_name == course):
            	   course_index_list.append(course_index)

            course_index_type_list = []
            for c in course_index_list:
            	course_index_type = CourseIndexType.objects.filter(course_index = c)
            	for ci in course_index_type:
            		course_index_type_list.append(ci)

            class_list = []
            for c in course_index_type_list:
            	class_session = Class.objects.filter(course_index_type = c)
            	for cs in class_session:
            		class_list.append(cs)

            attendance_list = []
            for c in class_list:
            	print (c,user)
            	attendance = Attendance.objects.get(class_session = c, student = user)
            	attendance_list.append(attendance)

            attendance_list = sorted(attendance_list, key=lambda r:r.class_session.datetime, reverse=True)
            
            for attendance in attendance_list:
                status = attendance.status
                time = attendance.attendance_time
                if (time):
                	time = time.strftime("%H:%M")
                else:
                	time = "__:__"

                class_session = attendance.class_session
                date = class_session.datetime.strftime("%d-%m-%y")

                course_index_type = class_session.course_index_type
                class_type = course_index_type.class_type
                _, hours, minutes, _, _ = _get_duration_components(course_index_type.duration)
                if (minutes == 0):
                	duration = f"{hours} hour(s)"
                elif (hours == 0):
                	duration = f"{minutes} minute(s)"
                else:
                	duration = f"{hours} hour(s) {minutes} minute(s)"

                course_index = course_index_type.course_index.index

                data_list.append({
                    'index':course_index,
                    'type':class_type,
                    'date':date,
                    'time':time,
                    'duration':duration,
                    'status':status
                    })

        data = {'state':state,
        'attendance':data_list
        }

        print (data)
        return JsonResponse(data)

class CourseStatsView(View):
    def post(self, request):
        body = json.loads(request.body)
        username = body.get('username')
        domain = body.get('domain')
        course = body.get('course')

        print(username,domain,course)
        try:
            user = UserLogin.objects.get(username=username)
            user = user.user
        except UserLogin.DoesNotExist:
            user = None

        state = False
        data_tut_list = []
        data_lab_list = []
        
        if (user and domain == "staff" and domain == user.domain):
            state = True

            class_instructor_list = ClassInstructor.objects.filter(staff=user)
            
            course_index_list = []
            for c in class_instructor_list:
                course_index = c.course_index
                if (course_index.course.course_name == course):
                    course_index_list.append(course_index)

            course_index_type_list = []
            for c in course_index_list:
            	course_index_type = CourseIndexType.objects.filter(course_index = c)
            	for ci in course_index_type:
            		course_index_type_list.append(ci)

            class_list = []
            for c in course_index_type_list:
            	class_session = Class.objects.filter(course_index_type = c)
            	for cs in class_session:
            		class_list.append(cs)

            class_list = sorted(class_list, key=lambda r:r.datetime, reverse=True)
            
            for c in class_list:
            	date = c.datetime.date().strftime("%d-%m-%y")
            	time = c.datetime.time().strftime("%H%M")
            	index = c.course_index_type.course_index.index

            	attendance_list = Attendance.objects.filter(class_session = c)
            	present = 0

            	for a in attendance_list:
                    if (a.status == "present"):
                	    present += 1
            	total = len(attendance_list)
            	rate = f"{present}/{total}"

            	class_type = c.course_index_type.class_type
            	course_code = c.course_index_type.course_index.course.course_code

            	if class_type == "lab":
            		data_lab_list.append({
            			'course_code':course_code,
	                	'index':index,
	                	'rate':rate,
	                	'date':date,
	                	'time':time
	                	})
            	elif class_type == "tutorial":
	            	data_tut_list.append({
	            		'course_code':course_code,
	                    'index':index,
	                    'rate':rate,
	                    'date':date,
	                    'time':time
	                    })

        data = {'state':state,
        'tut':data_tut_list,
        'lab':data_lab_list
        }

        print (data)
        return JsonResponse(data)


class SessionAttendanceView(View):
    def post(self, request):
        body = json.loads(request.body)
        index = body.get('index')
        date_str = body.get('date')

        print(index, date_str)
        try:
            course_index = CourseIndex.objects.get(index = index)
        except CourseIndex.DoesNotExist:
            course_index = None

        state = False
        data_list = []

        if (course_index):
        	state = True
        	date = datetime.datetime.strptime(date_str, "%d-%m-%y")
        	day = date.weekday()

        	try:
	        	course_index_type = CourseIndexType.objects.get(course_index = course_index, day = day)
	        	class_session = Class.objects.get(course_index_type = course_index_type, datetime__date = date)
	        	attendance_list = Attendance.objects.filter(class_session = class_session)

	        	for a in attendance_list:
	        		student = a.student
	        		name = student.name
	        		matric = student.matric_no
	        		status = a.status
	        		time = date_str
	        		signature = a.signature

	        		data_list.append({
	        			'name':name,
	        			'matric':matric,
	        			'status':status,
	        			'index':index,
	        			'time':time,
	                	'signature':signature
	        			})
        	except (CourseIndexType.DoesNotExist, Class.DoesNotExist, Attendance.DoesNotExist) as e:
        		state = False


        data = {'state':state,
        'student':data_list
        }

        print (data)
        return JsonResponse(data)

class OverwriteView(View):
    def post(self, request):
        body = json.loads(request.body)
        matric_no = body.get('matric')
        status = body.get('status')
        index = body.get('index')
        time = body.get('time')

        print(matric_no, status, index, time)
        course_name = ""

        try:
            course_index = CourseIndex.objects.get(index = index)
            course_name = course_index.course.course_name
        except CourseIndex.DoesNotExist:
            course_index = None

        state = False

        if (status != "present" and status != "mc" and status != "absent"):
        	data = {'state':state, 'course':course_name}
        	print (data)
        	return JsonResponse(data)

        if (course_index):
            date = datetime.datetime.strptime(time, "%d-%m-%y").date()

            try:
            	student = User.objects.get(matric_no = matric_no)

            	course_index_type = CourseIndexType.objects.filter(course_index = course_index)

            	class_session = None
            	for c in course_index_type:
	            	try:
	            	    class_session = Class.objects.get(course_index_type = c, datetime__date = date)
	            	    break
	            	except Class.DoesNotExist:
	            		pass

            	try:
	            	attendance = Attendance.objects.get(class_session = class_session, student = student)
	            	attendance.status = status
	            	attendance.save()
	            	state = True
            	except Attendance.DoesNotExist:
	            	pass

            except User.DoesNotExist:
           		pass

        data = {'state':state, 'course':course_name}
        print (data)
        return JsonResponse(data)




