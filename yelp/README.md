# Yelp-dataset
Final Examfor Databases course

The purpose of this project is to provide a web application for searching business by using
the Yelp dataset (see External Links section). From this page, a user can type the name of
a business, a category of interest and get the closest business to the specified one that
belong to the desired category.

To run the application perform the following steps:

1. From /yelp folder, set FLASK_APP environment variable: $export FLASK_APP='main.py'

2. From /yelp folder, execute the application by running the following command:
  - $python3 -m flask  run --host=0.0.0.0 --port=500X (where 500X is your assigned port number)

3. Open a browser (e.g. Chrome) and type: localhost:500X

4. If the application is not opened in your browser, create a tunnel to Flask. For so:
   - Being Loged out of Flask server, execute the line: ssh -4 -N -L 500X:localhost:500x user@flask01.network.ncf.edu

5. Open again your browser and enjoy the application!
