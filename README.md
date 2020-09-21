# multiple-choice-questions
A web application for conducting multiple choice questions assessment created to allow individuals and organisations to create assessments.

It allows assessment to be conducted within specified duration. 

Open submission of the assessment, score is calculated and feedback is returned telling the person when he passes or fails.

## How to run it on your local machine
To run this project on your machine, follow the following steps:

* Install python 3.6 and above (if you don't have)
* You also need to install __pip__ package manager
* Create a virtual environment using tool such as virtualenvs( assuming you don't have it and virtualenvswrapper installed) as follow:
```
    $ mkvirtualenv project-name
```
Running above command in the terminal will create and activate virtual environment with the given __project-name__.

* Clone the repository and cd into the project root directory:
```
    $ git clone repository url
    $ cd multiple-choice-questions
```

* Install all the dependencies:
```
    $ pip install -r requirements.txt 
```
* Finally, run the project( assuming all the previous steps were successful):
```
    $ python manage.py runserver
```
* Visit 127.0.0.0:8000  to view the multiple_choices application on your browser 
* Visit  127.0.0.0:8000/cbt/ to view the cbt application on your browser

# Hosting
* The projects with its two applications is hosted and can be visited through the following links:
    For multiple_choices application visit [here](https://multi-choices.herokuapp.com)
    while for cbt application visit [here](https://multi-choices.herokuapp.com/cbt/)

# License
This project is licenced under **MIT licence**.
