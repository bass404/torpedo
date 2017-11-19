runserver:
	export FLASK_APP=run.py && flask run

stopserver:
	sudo killall flask

startserver:
	export FLASK_APP=run.py && pipenv run nohup flask run &

restartserver: stopserver startserver
