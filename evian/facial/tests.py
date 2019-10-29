from django.test import TestCase
from login.models import User, UserLogin
from course.models import Course, CourseIndex, CourseIndexType, ClassTaker, ClassInstructor, Attendance, Class
import json
import datetime
import base64

# Create your tests here.
def createUser(matric="U1620136D", name="Jeko Lonardo", domain="student", img="test.jpg"):
	return User.objects.create(matric_no=matric, name=name, domain=domain, face_image=img)
def createUserLogin(user, username="jeko002",password="jeko002"):
	return UserLogin.objects.create(username=username, password=password, user=user)
def createCourse(code="CZ3002", name="Software Engineering"):
	return Course.objects.create(course_code=code, course_name=name)
def createCourseIndex(course, index="12345", group="CS1"):
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

class FacialViewTests(TestCase):
	def test_facial_tolerance_5_success_view(self):
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

		with open("test-valid.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':1,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "success")
		self.assertEqual(json_data["info"], "lt5")

	def test_facial_tolerance_5_multi_success_view(self):
		student1 = createUser()
		student2 = createUser(matric="U1620137D", name="Jeko Lonardo 2", domain="student", img="test.jpg")
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student1)
		createUserLogin(user=student2, username="jeko003", password="jeko003")
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student1)
		createClassTaker(course_index=course_index, student=student2)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student1)
		createAttendance(class_session=class_session, student=student2)

		with open("test-valid.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':1,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "warning")
		self.assertEqual(json_data["info"], "lt5")
		self.assertEqual(json_data["message"], "Multiple students recognized")

	def test_facial_tolerance_5_fail_view(self):
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

		with open("test-invalid.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':1,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["message"], "Authentication failed!")

	def test_facial_tolerance_5_no_face_view(self):
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

		with open("test-no-face.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':1,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["message"], "Authentication failed! No face detected")

	def test_facial_tolerance_5_multi_faces_view(self):
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

		with open("test-multi-faces.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':1,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["message"], "Authentication failed! Multiple faces detected")

	def test_facial_tolerance_6_success_view(self):
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

		with open("test-valid.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':4,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "success")
		self.assertEqual(json_data["info"], "lt6")

	def test_facial_tolerance_6_multi_success_view(self):
		student1 = createUser()
		student2 = createUser(matric="U1620137D", name="Jeko Lonardo 2", domain="student", img="test.jpg")
		staff = createUser(matric="S1620136D", name="Chris", domain="staff", img="test.jpg")
		createUserLogin(user=student1)
		createUserLogin(user=student2, username="jeko003", password="jeko003")
		createUserLogin(user=staff, username="chris002", password="chris002")
		course = createCourse()
		course_index = createCourseIndex(course=course)
		course_index_type = createCourseIndexType(course_index=course_index)
		class_session = createClass(course_index_type=course_index_type)
		createClassTaker(course_index=course_index, student=student1)
		createClassTaker(course_index=course_index, student=student2)
		createClassInstructor(course_index=course_index, staff=staff)
		createAttendance(class_session=class_session, student=student1)
		createAttendance(class_session=class_session, student=student2)

		with open("test-valid.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':4,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "warning")
		self.assertEqual(json_data["info"], "lt6")
		self.assertEqual(json_data["message"], "Multiple students recognized")

	def test_facial_tolerance_6_fail_view(self):
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

		with open("test-invalid.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':4,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["message"], "Authentication failed!")

	def test_facial_tolerance_6_no_face_view(self):
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

		with open("test-no-face.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':4,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["message"], "Authentication failed! No face detected")

	def test_facial_tolerance_6_multi_faces_view(self):
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

		with open("test-multi-faces.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':4,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["message"], "Authentication failed! Multiple faces detected")

	def test_facial_invalid_count_view(self):
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

		with open("test-valid.jpg", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':7,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["info"], "error-count")

	def test_facial_invalid_image_view(self):
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

		encoded_string = ""

		response = self.client.post("/facial/",json.dumps({'count':1,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["info"], "error-image")

	def test_facial_sign_success_view(self):
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

		with open("sign.png", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':6,'matric':'U1620136D','image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "success")

	def test_facial_sign_invalid_image_view(self):
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

		encoded_string = ""

		response = self.client.post("/facial/",json.dumps({'count':6,'matric':'U1620136D','image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["info"], "error-image")

	def test_facial_sign_no_matric_view(self):
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

		with open("sign.png", "rb") as img_file:
			encoded_string = base64.b64encode(img_file.read())

		encoded_string = encoded_string.decode("utf-8")

		encoded_string = "data:image/jpeg;base64,"+encoded_string

		response = self.client.post("/facial/",json.dumps({'count':6,'image':encoded_string}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], "error")
		self.assertEqual(json_data["info"], "error-matric")
		
		
