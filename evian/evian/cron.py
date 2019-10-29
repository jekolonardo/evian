from django_cron import CronJobBase, Schedule
from course.models import Course, CourseIndex, CourseIndexType, ClassTaker, Class, Attendance
from login.models import User
import datetime

class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 1

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

	code = "evian.my_cron_job"

	def do(self):
		# print("test")
		tdelta = (3 - datetime.datetime.today().weekday()) % 7
		today_date = datetime.datetime.now().date() + datetime.timedelta(days=tdelta)

		# today_date = datetime.datetime.now().date()
		
		day = today_date.weekday()
		course_index_type_list = CourseIndexType.objects.filter(day = day)

		for c in course_index_type_list:
			date_time = datetime.datetime.combine(today_date, c.time)
			try:
				class_session = Class.objects.get(course_index_type = c, datetime = date_time)
			except Class.DoesNotExist:
				class_session = Class(course_index_type = c, datetime = date_time)
				class_session.save()
				class_taker_list = ClassTaker.objects.filter(course_index = c.course_index)

				for ct in class_taker_list:
					attendance = Attendance(class_session = class_session, student = ct.student, status="absent")
					attendance.save()



