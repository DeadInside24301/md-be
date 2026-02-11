Backend for my inventory system made from Python Flask and uses RESTFul Api's

Required to Install first

Python 3.10 

pip any version (a new pip will be installed and used in venv)

Installation and Setup

1.) Clone the repository using 'git clone', then navigate to the project directory using 'cd'.

2.) Create the the venv by using this command 'python -m venv venv'

3.) Activate venv by using 'source venv/Scripts/activate' (command may differ depending on the vs code terminal)(i use bash)

4.) Install the requirements by using 'pip install -r requirements.txt'

5.) Configure the interpreter by using ctrl + shift + p and type interpreter, select python interpreter and locate the python application within the projects venv folder (usually in C:\Users\[pcname]\[parent directory]\[Directory]\[project backend]\venv\Scripts\)

6.) Create an '.env' file in the root directory and configure the required environment variables.

7.) Start the development server using 'python run.py'.

For Database

Requirements

PostgreSQL

pgAdmin 4

How to install

Open pgAdmin and select a server then create a database

Right Click on the created Database the click restore

Locate the sql file

Then click restore

Check if tables are in Schema > public > Tables 
