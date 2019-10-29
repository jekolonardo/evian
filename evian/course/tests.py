from django.test import TestCase
from login.models import User, UserLogin
from .models import Course, CourseIndex, CourseIndexType, ClassTaker, ClassInstructor, Attendance, Class
import json
import datetime

# Create your tests here.
def createUser(matric="U1620136D", name="Jeko Lonardo", domain="student", img="test.jpg"):
	return User.objects.create(matric_no=matric, name=name, domain=domain, face_image=img)
def createUserLogin(user, username="jeko002",password="jeko002"):
	return UserLogin.objects.create(username=username, password=password, user=user)
def createCourse(code="CZ2006", name="Software Engineering"):
	return Course.objects.create(course_code=code, course_name=name)
def createCourseIndex(course, index="54321", group="CS1"):
	return CourseIndex.objects.create(course=course, index=index, group=group)
def createCourseIndexType(course_index, class_type="lab", day=3, time="10:30", duration=2):
	time = datetime.datetime.strptime(time,"%H:%M").time()
	duration = datetime.timedelta(hours=duration)
	return CourseIndexType.objects.create(course_index=course_index, class_type=class_type, day=day, time=time, duration=duration)
def createClass(course_index_type, time="10:30"):
	tdelta = (3 - datetime.datetime.today().weekday()) % 7
	today_date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
	time = datetime.datetime.strptime(time,"%H:%M").time()
	dt = datetime.datetime.combine(today_date, time)
	return Class.objects.create(course_index_type=course_index_type, datetime=dt)
def createClassTaker(course_index, student):
	return ClassTaker.objects.create(course_index=course_index, student=student)
def createClassInstructor(course_index, staff):
	return ClassInstructor.objects.create(course_index=course_index, staff=staff)
def createAttendance(class_session, student, status="present", attendance_time="10:40"):
	if not attendance_time:
		return Attendance.objects.create(class_session=class_session, student=student, status=status)
	attendance_time = datetime.datetime.strptime(attendance_time,"%H:%M").time()
	return Attendance.objects.create(class_session=class_session, student=student, status=status, attendance_time=attendance_time)

class AttendanceViewTests(TestCase):
	def test_attendance_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/attendance/",json.dumps({'username':'jeko002','domain':'student','course':'Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], True)
		self.assertEqual(len(json_data["attendance"]), 1)

	def test_attendance_wrong_username_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/attendance/",json.dumps({'username':'jeko003','domain':'student','course':'Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_attendance_wrong_domain_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/attendance/",json.dumps({'username':'jeko002','domain':'staff','course':'Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_attendance_no_course_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/attendance/",json.dumps({'username':'jeko002','domain':'student','course':'Advanced Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], True)
		self.assertEqual(len(json_data["attendance"]), 0)

class CourseStatsViewTests(TestCase):
	def test_course_stats_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/course-stats/",json.dumps({'username':'chris002','domain':'staff','course':'Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], True)
		self.assertEqual(len(json_data["lab"]), 1)

	def test_course_stats_wrong_username_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/course-stats/",json.dumps({'username':'chris003','domain':'staff','course':'Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_course_stats_wrong_domain_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/course-stats/",json.dumps({'username':'chris002','domain':'student','course':'Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_course_stats_no_course_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		response = self.client.post("/course-stats/",json.dumps({'username':'chris002','domain':'staff','course':'Advanced Software Engineering'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], True)
		self.assertEqual(len(json_data["lab"]), 0)
		self.assertEqual(len(json_data["tut"]), 0)

class SessionAttendanceViewTests(TestCase):
	def test_session_attendance_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		tdelta = (3 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/session-attendance/",json.dumps({'index':'54321', 'date':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], True)

	def test_session_attendance_wrong_index_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		tdelta = (3 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/session-attendance/",json.dumps({'index':'54322', 'date':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_session_attendance_wrong_date_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student)

		tdelta = (2 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/session-attendance/",json.dumps({'index':'54321', 'date':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)


class OverwriteViewTests(TestCase):
	def test_overwrite_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student, status="absent", attendance_time="")

		tdelta = (3 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/overwrite/",json.dumps({'matric':'U1620136D', 'status':'mc', 'index' : '54321', 'time':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], True)

	def test_overwrite_wrong_matric_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student, status="absent", attendance_time="")

		tdelta = (3 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/overwrite/",json.dumps({'matric':'U1620137D', 'status':'mc', 'index' : '54321', 'time':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_overwrite_wrong_status_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student, status="absent", attendance_time="")

		tdelta = (3 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/overwrite/",json.dumps({'matric':'U1620136D', 'status':'late', 'index' : '54321', 'time':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_overwrite_wrong_index_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student, status="absent", attendance_time="")

		tdelta = (3 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/overwrite/",json.dumps({'matric':'U1620136D', 'status':'mc', 'index' : '54322', 'time':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_overwrite_wrong_time_view(self):
		student = createUser()
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student)
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student, status="absent", attendance_time="")

		tdelta = (2 - datetime.datetime.today().weekday()) % 7
		date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)
		date = datetime.datetime.strftime(date, "%d-%m-%y")

		response = self.client.post("/overwrite/",json.dumps({'matric':'U1620136D', 'status':'mc', 'index' : '54321', 'time':date}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)
	