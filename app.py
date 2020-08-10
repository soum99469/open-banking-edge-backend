from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime 
import pytz 

IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)

app = Flask(__name__)

Edge_Client = MongoClient('mongodb://localhost:27017')
Edge_BankDB = Edge_Client['Edge_BankDB']
Edge_Accounts = Edge_BankDB['Edge_Accounts']

Main_Client = MongoClient('mongodb://localhost:27017')
Main_BankDB = Main_Client['Main_BankDB']
Main_Accounts = Main_BankDB['Main_Accounts']

@app.route("/create_account")
def create_account():
	data = { 
		"_id" : "100",
		"Account" : 
		{
			"Brach Code" : "ICICI_002", 
			"Account No" : "100",
			"TOA" : "Savings"
		},
		"User" : 
		{
			"FName" : "IAmUser",
			"DOB" : "01-01-2001",
			"FatherNmae" : "IAmFather"
		},
		"Occupation" :
		{
		"Type" : "Salary",
		"Status" : "active",
		"Annual Income" : "100000",
		"Nationality" : "Indian"
		},
		"Address" :
		{
		"FlatNo" : "5",
		"StreetNo" : "6",
		"City" : "Pune",
		"District" : "Maharashtra",
		"State" : "Shivaji Road",
		"Country" : "India",
		"PinCode" : "500004"
		},
		"Contact" :
		{
		"Telephone" : "011-5664-2999",
		"Mobile" : "9876543210"
		},
		"Updated" :
		{
		"Updated Date" : datetime_ist.strftime('%d-%m-%Y %H:%M:%S %Z %z'),
		"Updated By" : "test_user",
		"Processed Indicator" : "NI"
		}
	}

	if(Edge_Accounts.count_documents({}) == 0):
		Edge_Accounts.insert_one(data)

	else:
		last_data = Edge_Accounts.find().sort([('_id',-1)]).limit(1)

		for d in last_data:
			acc_no = d["_id"]

		data["_id"] = str(int(acc_no) + 1)
		data["Account"]["Account No"] = data["_id"]	

		Edge_Accounts.insert_one(data)

		data["_id"] = "100"
		data["Account"]["Account No"] = "100"
	
	s="<p>"
	for x in Edge_Accounts.find():
		s = s + str(x) + "<br><br><br>"
	s+="</p>"
	return s


@app.route("/syncdb")
def syncdb():
	for x in Edge_Accounts.find():
		if (x["Updated"]["Processed Indicator"] != "I"):
			x["Updated"]["Processed Indicator"] = "I"
			Edge_Accounts.update_one({"_id" : x["_id"]},{"$set" : {"Updated" : x["Updated"]}})
			Main_Accounts.insert_one(x)

	return "<h1>Synced till Account Number : "+ x["_id"] +" !!!</h1>"


app.run(host="0.0.0.0", port=5000)