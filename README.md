Make sure conda@4.7.10 is installed
Make sure npm is installed

create environment:
	conda create --name evianenv
activate environment:
	conda activate evianenv
install pip and dlib in conda:
	conda install pip
	conda install -c conda-forge dlib	

Open 2 command line, one to evian, another to evian-react

in evian:
install requirements.txt
	pip install -r requirements.txt

in evian-react:
install dependencies
	npm install

in evian:
run server:
	python manage.py runserver

in evian-react:
run client:
	npm start

access localhost:3000 for login (for student: user : jeko001 ; pass : jeko001, for staff: user : paul001 ; pass : paul001)
access localhost:3000/facial for facial recognition

To see student/staff login credential:
1. go to localhost:8000/admin user:jekol pass:jekol
2. go to UserLogin
