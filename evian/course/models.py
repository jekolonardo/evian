from django.db import models
from login.models import User
DAYS=[
(0,'Monday'),
(1,'Tuesday'),
(2,'Wednesday'),
(3,'Thursday'),
(4,'Friday'),
(5,'Saturday'),
(6,'Sunday')
]

CLASS_TYPE = [
('lecture','Lecture'),
('tutorial','Tutorial'),
('lab','Lab')
]

STATUS = [
('present','Present'),
('absent','Absent'),
('mc','MC')
]

# Create your models here.
class Course(models.Model):
	course_code = models.CharField(max_length=10)
	course_name = models.CharField(max_length=100)

	def __str__(self):
		return self.course_code

class CourseIndex(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	index = models.CharField(max_length=10)
	group = models.CharField(max_length=10)

	def __str__(self):
		return f'{str(self.course)}-{self.index}'

	class Meta:
		verbose_name_plural = "Course Indexes"

class CourseIndexType(models.Model):
	course_index = models.ForeignKey(CourseIndex, on_delete=models.CASCADE)
	class_type = models.CharField(max_length=10, choices=CLASS_TYPE)
	day = models.IntegerField(choices=DAYS)
	time = models.TimeField('class time')
	duration = models.DurationField()

	def __str__(self):
		return f'{str(self.course_index)}-{self.class_type}'

class Class(models.Model):
	course_index_type = models.ForeignKey(CourseIndexType, on_delete=models.CASCADE)
	datetime = models.DateTimeField('class datetime')
	def __str__(self):
		return f'{str(self.course_index_type)}-{self.datetime.date()}-{self.datetime.time()}'
	class Meta:
		verbose_name_plural = "Classes"

class ClassTaker(models.Model):
	course_index = models.ForeignKey(CourseIndex, on_delete=models.CASCADE)
	student = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	# matric_no = models.CharField(max_length=20)
	def __str__(self):
		return f'{str(self.course_index)}-{str(self.student)}'

class ClassInstructor(models.Model):
	course_index = models.ForeignKey(CourseIndex, on_delete=models.CASCADE)
	staff = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return f'{str(self.course_index)}-{str(self.staff)}'

class Attendance(models.Model):
	class_session = models.ForeignKey(Class, on_delete=models.CASCADE)
	student = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	status = models.CharField(max_length=10, choices=STATUS)
	attendance_time = models.TimeField('attendance time', null=True, blank=True)
	signature = models.TextField(blank=True, default='')

	def __str__(self):
		return f'{str(self.class_session)}-{str(self.student)}'






