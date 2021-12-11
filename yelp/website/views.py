from flask import Blueprint, render_template, request
import psycopg2
import pandas as pd

conn = psycopg2.connect(dbname='yelpDb')
cur = conn.cursor()

#Given a business name, retrieves its id
def getBusinessId(businessName):
  #id = '-s3nJbZRXLMSpwud22iIPA'
  cur.execute("select id from business_category where name = '{businessName}' limit 1;")
  result = cur.fetchall()
  id=''
  for row in result:
   id = row[0]
   
  return id

#Given a business id and its category, retrieve the closest
#business of the specified category
def generateBusinessQuery(business_id, type):

  print("User Input: ", business_id, type)
  type = 'Restaurants'
  
  #Get position of the business received as parameter (user's input)
  #location_query = "select latitude, longitude from business_category where id = '-s3nJbZRXLMSpwud22iIPA';"
  location_query = "select latitude, longitude from business_category where id = '{business_id}';"
  print("---Execute query: ", location_query)
  cur.execute(location_query)
  location = cur.fetchall()
  #print("Location query result: ", location)
  #Get latitude and longitude of the business from the retrieved query
  #lat = 40.3862
  #long = -79.8219
  #Initialize lat and long
  lat = 0
  long = 0
  #Store retrieved latitude and longitude values of the business
  for row in location:
    lat = row[0]
    long = row[1]
  
  query = "select name, category, ( point(latitude, longitude) <-> point(%s, %s) )*111.325 AS distance, stars from business_category where category = 'Restaurants' order by distance limit 10;"
  #query = "select * from business_category limit 5;"
  print("---Execute query: ", query)
  cur.execute(query, (lat, long))
  result = cur.fetchall()
  #print("Final query result: ", result)
  return result

#Generate results table from the result of the query
def generateBusinessTable(data):
  headings = ("Name", "Category", "Distance", "Stars")
  data_list=list()

  for row in data:
    data_list.append(row)

  data=tuple(data_list)
  #Harcoded data for testing purpose
  #data = (("Kentucky Fried Chicken", "Restaurant", "100 miles", "4/5"),
	 # ("Chipplotle", "Restaurant", "150 miles", "4/5"),
         # ("McDonald's", "Restaurant", "500 miles", "3.5/5"),
         # ("Burger King", "Restaurant", "750 miles", "5/5"),
         # ("IHopp", "Restaurant", "780 miles", "4.2/5"))

  return headings, data

#Get available business names within the database.
#Will be used to autocomplete the user's input
def getAvailableBusiness():
  #Retrieve bussiness names available in the database
  query = 'select distinct(name) from business;'
  print("---Execute query: ", query)
  cur.execute(query)
  business_options = cur.fetchall()
  data_list=list()

  for row in business_options:
    data_list.append(row)
  business_options=tuple(data_list)
  #print(business_options)

  return business_options

views = Blueprint('views', __name__)
@views.route('/')
def home():
  return render_template("home.html")

@views.route('/search-business', methods=['GET', 'POST'])
def search_business():
  if request.method == "GET":
   # Retrieve all the business from the database to autocomplete user's input
    business_options = getAvailableBusiness()
    return render_template("search_business.html", business_options=business_options)
  else:
    business = request.form.get('business', default=None, type=str)
    type = request.form.get('type', default=None)
    print("Users Type: ", type)
    #Get business identifier
    business_id = getBusinessId(business)
    print("Users business id: ",business_id)
    #Get from the DB the closest business of the specified type entered by the user
    result = generateBusinessQuery(business_id, type)
    print(result)
    #Generate table of results
    headings, data = generateBusinessTable(result)
    return render_template("search_business.html", headings=headings, data=data)

