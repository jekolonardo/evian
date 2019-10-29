from django.core.management.base import BaseCommand, CommandError
from course.models import Course, CourseIndex, CourseIndexType, ClassTaker, Class, Attendance
from login.models import User
import datetime

class Command(BaseCommand):
	today = datetime.datetime.now()
	today_date = today.date()+datetime.timedelta(days=1)
	today_time = today.time()
	help = "generate new class sessions for "+datetime.datetime.strftime(today_date, "%d-%m-%y")

	def handle(self, *args, **options):
		print("Generating classes")
		date = datetime.datetime.now().date()
		self.generate_class(date)

	def generate_class(self, date):
		
		day = date.weekday()
		course_index_type_list = CourseIndexType.objects.filter(day = day)

		for c in course_index_type_list:
			date_time = datetime.datetime.combine(date, c.time)
			try:
				class_session = Class.objects.get(course_index_type = c, datetime = date_time)
			except Class.DoesNotExist:
				class_session = Class(course_index_type = c, datetime = date_time)
				class_session.save()
				class_taker_list = ClassTaker.objects.filter(course_index = c.course_index)

				for ct in class_taker_list:
					attendance = Attendance(class_session = class_session, student = ct.student, status="absent")
					attendance.save()



