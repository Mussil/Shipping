"# Shipping" 

############ First run ###################
Windows: 
run these commands:
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run

if you get an error you are not on development environment try these commands:
> py -3 -m venv venv
and then activate virtual environment:
> venv\Scripts\activate
if you get an error try:
> Set-ExecutionPolicy Unrestricted -Scope Process
and then try again:
> venv\Scripts\activate
you should get '(venv)' in your terminal 

