from django.test import TestCase
from .models import User, UserLogin
import json

# Create your tests here.
def createUser(matric="U1620136D", name="Jeko Lonardo", domain="student", img="test.jpg"):
	return User.objects.create(matric_no=matric, name=name, domain=domain, face_image=img)
def createUserLogin(user, username="jeko002",password="jeko002"):
	return UserLogin.objects.create(username=username, password=password, user=user)

class UserLoginViewTests(TestCase):
	def test_success_login(self):
		createUserLogin(user=createUser())
		response = self.client.post("/login/",json.dumps({'username':'jeko002','password':'jeko002'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], True)

	def test_wrong_username_login(self):
		createUserLogin(user=createUser())
		response = self.client.post("/login/",json.dumps({'username':'jeko001','password':'jeko002'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)

	def test_wrong_password_login(self):
		createUserLogin(user=createUser())
		response = self.client.post("/login/",json.dumps({'username':'jeko002','password':'jeko001'}),'json')
		self.assertEqual(response.status_code, 200)
		json_data = json.loads(response.content)
		self.assertEqual(json_data["state"], False)






