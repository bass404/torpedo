runserver:
	export FLASK_APP=run.py && flask run

start_server:
	export FLASK_APP=run.py && pipenv run nohup flask run &
