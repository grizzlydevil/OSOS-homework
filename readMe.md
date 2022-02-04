to add this repository -> git clone https://github.com/grizzlydevil/OSOS-homework.git

decathlon.py -> the main logic for getting the csv file, processing it and exporting
decathlon_test.py -> for running tests
to run tests enter in terminal -> python -m unittest decathlon_test.py

To open in browser these needs to be installed:
pip install flask
pip install flask-wtf

the logic is in ./app folder

command to run the server -> flask run

open form in browser: http://127.0.0.1:5000/

browse and submit a scv file.
the results will be exported to flaskFile.json
