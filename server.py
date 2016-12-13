#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import string
import traceback
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
DATABASEURI = "postgresql://sz2539:0034@w4111vm.eastus.cloudapp.azure.com/w4111"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#

# I set them as comment by myself

#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

"""
@app.route('/')
def index():
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data


  # DEBUG: this is debugging code to see what request looks like
  print request.args
"""

  #
  # example of a database query
  #

"""
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
"""
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  #return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#





#I think I should start here

@app.route('/')
def index():
  return render_template("index.html")



############################---------index.html-----------#####################
#change to another website
@app.route('/another')
def another():
  return render_template("another.html")

@app.route('/Login')
def Login():
  account = request.args.get('account')
  password = request.args.get('password')
  if account == "SZandJZ" and password == "Databases4111":
    return render_template("Login.html")
  else:
    return render_template("index.html")

@app.route('/Query')
def Query():
  return render_template("Query.html")




############################---------Login.html-----------#####################
#Add SHIELDMember(SID, SName, SAge, SGender, SAbility)
@app.route('/addSagent', methods=['POST'])
def addSagent():
  try:
    SID = str(request.form['SID'])
    SName = str(request.form['SName'])
    SAge = str(request.form['SAge'])
    SGender = str(request.form['SGender'])
    SAbility = str(request.form['SAbility'])

    engine.connect().execute("INSERT INTO SHIELDMember(SID, SName, SAge, SGender, SAbility) VALUES (\'" + SID + "\',\'" + SName + "\',\'" + SAge + "\',\'" + SGender + "\',\'" + SAbility + "\');")
    return render_template("Login.html")

  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add HYDRAMember(HID, HName, HAge, HGender, HAbility)
@app.route('/addHagent', methods=['POST'])
def addHagent():
  try:
    HID = str(request.form['HID'])
    HName = str(request.form['HName'])
    HAge = str(request.form['HAge'])
    HGender = str(request.form['HGender'])
    HAbility = str(request.form['HAbility'])
    engine.connect().execute("INSERT INTO HYDRAMember(HID, HName, HAge, HGender, HAbility) VALUES (\'" + HID + "\',\'" + HName + "\',\'" + HAge + "\',\'" + HGender + "\',\'" + HAbility + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add INHUMANMember(IID, IName, IAge, IGender, IAbility)
@app.route('/addIagent', methods=['POST'])
def addIagent():
  try:
    IID = str(request.form['IID'])
    IName = str(request.form['IName'])
    IAge = str(request.form['IAge'])
    IGender = str(request.form['IGender'])
    IAbility = str(request.form['IAbility'])
    engine.connect().execute("INSERT INTO INHUMANSMember(IID, IName, IAge, IGender, IAbility) VALUES (\'" + IID + "\',\'" + IName + "\',\'" + IAge + "\',\'" + IGender + "\',\'" + IAbility + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add Mission(MID, MName, MTimestart, MTimeend, MDescription)
@app.route('/addMission', methods=['POST'])
def addMission():
  try:
    MID = str(request.form['MID'])
    MName = str(request.form['MName'])
    MTimestart = str(request.form['MTimestart'])
    MTimeend = str(request.form['MTimeend'])
    MDescription = str(request.form['MDescription'])
    engine.connect().execute("INSERT INTO Mission(MID, MName, MTimestart, MTimeend, MDescription) VALUES (\'" + MID + "\',\'" + MName + "\',\'" + MTimestart + "\',\'" + MTimeend + "\',\'" + MDescription + "\');")
  #return MDescription
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add ValuableItem(VID, VName, VFunction)
@app.route('/addValuableItem', methods=['POST'])
def addValuableItem():
  try:
    VID = str(request.form['VID'])
    VName = str(request.form['VName'])
    VFunction = str(request.form['VFunction'])
    engine.connect().execute("INSERT INTO ValuableItem(VID, VName, VFunction) VALUES (\'" + VID + "\',\'" + VName + "\',\'" + VFunction + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add Facility(FID, FName, FFunction)
@app.route('/addFacility', methods=['POST'])
def addFacility():
  try:
    FID = str(request.form['FID'])
    FName = str(request.form['FName'])
    FFunction = str(request.form['FFunction'])
    engine.connect().execute("INSERT INTO Facility(FID, FName, FFunction) VALUES (\'" + FID + "\',\'" + FName + "\',\'" + FFunction + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'


#Add Duty(DID, DName, DFunction)
@app.route('/addDuty', methods=['POST'])
def addDuty():
  try:
    DID = str(request.form['DID'])
    DName = str(request.form['DName'])
    DFunction = str(request.form['DFunction'])
    engine.connect().execute("INSERT INTO Duty(DID, DName, DFunction) VALUES (\'" + DID + "\',\'" + DName + "\',\'" + DFunction + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add Relationship1(SID, HID, R)
@app.route('/addRelationship1', methods=['POST'])
def addRelationship1():
  try:
    SID = str(request.form['SID'])
    HID = str(request.form['HID'])
    R = str(request.form['R'])
    engine.connect().execute("INSERT INTO Relationship1(SID, HID, R) VALUES (\'" + SID + "\',\'" + HID + "\',\'" + R + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add Relationship2(SID, IID, R)
@app.route('/addRelationship2', methods=['POST'])
def addRelationship2():
  try:
    SID = str(request.form['SID'])
    IID = str(request.form['IID'])
    R = str(request.form['R'])
    engine.connect().execute("INSERT INTO Relationship2(SID, IID, R) VALUES (\'" + SID + "\',\'" + IID + "\',\'" + R + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add Relationship3(IID, HID, R)
@app.route('/addRelationship3', methods=['POST'])
def addRelationship3():
  try:
    IID = str(request.form['IID'])
    HID = str(request.form['HID'])
    R = str(request.form['R'])
    engine.connect().execute("INSERT INTO Relationship3(IID, HID, R) VALUES (\'" + IID + "\',\'" + HID + "\',\'" + R + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add Participate1(SID, MID, Timestart, Timeend)
@app.route('/addParticipate1', methods=['POST'])
def addParticipate1():
  try:
    SID = str(request.form['SID'])
    MID = str(request.form['MID'])
    Timestart = str(request.form['Timestart'])
    Timeend = str(request.form['Timeend'])
    engine.connect().execute("INSERT INTO Participate1(SID, MID, Timestart, Timeend) VALUES (\'" + SID + "\',\'" + MID + "\',\'" + Timestart + "\',\'" + Timeend + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add Participate2(HID, MID, Timestart, Timeend)
@app.route('/addParticipate2', methods=['POST'])
def addParticipate2():
  try:
    HID = str(request.form['HID'])
    MID = str(request.form['MID'])
    Timestart = str(request.form['Timestart'])
    Timeend = str(request.form['Timeend'])
    engine.connect().execute("INSERT INTO Participate2(HID, MID, Timestart, Timeend) VALUES (\'" + HID + "\',\'" + MID + "\',\'" + Timestart + "\',\'" + Timeend + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add addBelongsTo(SID, FID)
@app.route('/addBelongsTo', methods=['POST'])
def addBelongsTo():
  try:
    SID = str(request.form['SID'])
    FID = str(request.form['FID'])
    engine.connect().execute("INSERT INTO BelongsTo(SID, FID) VALUES (\'" + SID + "\',\'" + FID + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add addServeAs(SID, DID)
@app.route('/addServeAs', methods=['POST'])
def addServeAs():
  try:
    SID = str(request.form['SID'])
    DID = str(request.form['DID'])
    engine.connect().execute("INSERT INTO ServeAs(SID, DID) VALUES (\'" + SID + "\',\'" + DID + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Add addAppearance(MID, VID)
@app.route('/addAppearance', methods=['POST'])
def addAppearance():
  try:
    MID = str(request.form['MID'])
    VID = str(request.form['VID'])
    engine.connect().execute("INSERT INTO Appearance(MID, VID) VALUES (\'" + MID + "\',\'" + VID + "\');")
    return render_template("Login.html")
  except Exception, e:
    print traceback.print_exc()
    return '1'


############################---------query.html-----------#####################
##################--------Query
@app.route('/QuerySubmit')
def QuerySubmit():
  try:
    querys = str(request.args.get('querys'))
    if querys[0] == 'C' or querys[0] == 'I':
    	return "You are not an admin!"
    else:
	    rows = g.conn.execute(querys)
	    #rows = querysql(querys)
	    result = ""
	    #res = []
	    for row in rows:
	      s = str(row)
	      st = "[" + strfun(s) + "] " + "\n"
	      result = result + st
	    return result
  except Exception, e:
    print traceback.print_exc()
    return '1'

##################--------Search
#Search for SHIELD Member
@app.route('/SearchSMember')
def SearchSMember():
  try:
    SID = str(request.args.get('SID'))
    SName = str(request.args.get('SName'))
    result = ""
    if len(SID) == 0:
      sexecute = "SELECT S.SID FROM SHIELDMember S WHERE S.SName=\'" + SName + "\'"
      profiles = g.conn.execute(sexecute)
      for profile in profiles:
        SID = str(profile)
        SID = strfun(SID)
      SID = SID[0: len(SID) - 1]
    
    #profile
    sexecute = "SELECT S.SID, S.SName, S.SAge, S.SGender, S.SAbility  FROM SHIELDMember S WHERE S.SID=\'" + SID + "\'"
    profiles = g.conn.execute(sexecute)
    for profile in profiles:
      s = str(profile)
      st = "Profile: [" + strfun(s) + "]------------- " + "\n"
      result = result + st
    #mission
    sexecute = "SELECT M.MID, M.MName FROM Mission M, Participate1 P1 WHERE P1.SID=\'" + SID + "\' AND P1.MID = M.MID"  
    missions = g.conn.execute(sexecute)
    result = result + "Mission: "
    for mission in missions:
      s = str(mission)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    #HYDRA relationship
    sexecute = "SELECT R1.HID, H.HName, R1.R FROM HYDRAMember H, Relationship1 R1 WHERE R1.SID=\'" + SID + "\' AND H.HID = R1.HID" 
    HRs = g.conn.execute(sexecute)
    result = result + "HYDRA Relationship: "
    for HR in HRs:
      s = str(HR)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    #INHUMAN relationship
    sexecute = "SELECT R2.IID, I.IName, R2.R FROM Relationship2 R2, INHUMANSMember I WHERE R2.SID=\'" + SID + "\' AND I.IID=R2.IID"
    IRs = g.conn.execute(sexecute)
    result = result + "INHUMAN Relationship: "
    for IR in IRs:
      s = str(IR)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    #Facility
    sexecute = "SELECT B.FID, F.FName FROM BelongsTo B, Facility F WHERE B.SID=\'" + SID + "\' AND B.FID=F.FID"
    Fas = g.conn.execute(sexecute)
    result = result + "Facility: "
    for Fa in Fas:
      s = str(Fa)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    return result
    
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Search for HYDRA Member
@app.route('/SearchHMember')
def SearchHMember():
  try:
    HID = str(request.args.get('HID'))
    HName = str(request.args.get('HName'))
    result = ""
    if len(HID) == 0:
      sexecute = "SELECT H.HID FROM HYDRAMember H WHERE H.HName=\'" + HName + "\'"
      profiles = g.conn.execute(sexecute)
      for profile in profiles:
        HID = str(profile)
        HID = strfun(HID)
      HID = HID[0: len(HID) - 1]

    #profile
    sexecute = "SELECT H.HID, H.HName, H.HAge, H.HGender, H.HAbility  FROM HYDRAMember H WHERE H.HID=\'" + HID + "\'"
    profiles = g.conn.execute(sexecute)
    for profile in profiles:
      s = str(profile)
      st = "Profile: [" + strfun(s) + "]------------- " + "\n"
      result = result + st
    
    #mission
    sexecute = "SELECT M.MID, M.MName FROM Mission M, Participate2 P2 WHERE P2.HID=\'" + HID + "\' AND P2.MID = M.MID"  
    missions = g.conn.execute(sexecute)
    result = result + "Mission: "
    for mission in missions:
      s = str(mission)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    #SHIELD relationship
    sexecute = "SELECT R1.SID, S.SName, R1.R FROM SHIELDMember S, Relationship1 R1 WHERE R1.HID=\'" + HID + "\' AND S.SID = R1.SID" 
    SRs = g.conn.execute(sexecute)
    result = result + "HYDRA Relationship: "
    for SR in SRs:
      s = str(SR)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    #INHUMAN relationship
    sexecute = "SELECT R3.IID, I.IName, R3.R FROM Relationship3 R3, INHUMANSMember I WHERE R3.HID=\'" + HID + "\' AND I.IID=R3.IID"
    IRs = g.conn.execute(sexecute)
    result = result + "INHUMAN Relationship: "
    for IR in IRs:
      s = str(IR)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    return result
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Search for INHUMAN Member
@app.route('/SearchIMember')
def SearchIMember():
  try:
    IID = str(request.args.get('IID'))
    IName = str(request.args.get('IName'))
    result = ""
    if len(IID) == 0:
      sexecute = "SELECT I.IID FROM INHUMANSMember I WHERE I.IName=\'" + IName + "\'"
      profiles = g.conn.execute(sexecute)
      for profile in profiles:
        IID = str(profile)
        IID = strfun(IID)
      IID = IID[0: len(IID) - 1]

    #profile
    sexecute = "SELECT I.IID, I.IName, I.IAge, I.IGender, I.IAbility  FROM INHUMANSMember I WHERE I.IID=\'" + IID + "\'"
    profiles = g.conn.execute(sexecute)
    for profile in profiles:
      s = str(profile)
      st = "Profile: [" + strfun(s) + "]------------- " + "\n"
      result = result + st
    
    #SHIELD relationship
    sexecute = "SELECT R2.SID, S.SName, R2.R FROM SHIELDMember S, Relationship2 R2 WHERE R2.IID=\'" + IID + "\' AND S.SID = R2.SID" 
    SRs = g.conn.execute(sexecute)
    result = result + "SHIELD Relationship: "
    for SR in SRs:
      s = str(SR)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    #HYDRA relationship
    sexecute = "SELECT R3.HID, H.HName, R3.R FROM Relationship3 R3, HYDRAMember H WHERE R3.IID=\'" + IID + "\' AND H.HID=R3.HID"
    HRs = g.conn.execute(sexecute)
    result = result + "HYDRA Relationship: "
    for HR in HRs:
      s = str(HR)
      st = "[" + strfun(s) + "]    " + "\n"
      result = result + st
    result = result + "--------------- "
    return result
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Search for Mission
@app.route('/SearchMission')
def SearchMission():
  try:
    MID = str(request.args.get('MID'))
    MName = str(request.args.get('MName'))
    result = ""
    if len(MID) == 0:
      sexecute = "SELECT M.MID FROM Mission M WHERE M.MName=\'" + MName + "\'"
      profiles = g.conn.execute(sexecute)
      for profile in profiles:
        MID = str(profile)
        MID = strfun(MID)
      MID = MID[0: len(MID) - 1]

    #profile
    sexecute = "SELECT M.MID, M.MName, M.MTimestart, M.MTimeend, M.MDescription  FROM Mission M WHERE M.MID=\'" + MID + "\'"
    profiles = g.conn.execute(sexecute)
    for profile in profiles:
      s = str(profile)
      st = "Profile: [" + strfun(s) + "]------------- " + "\n"
      result = result + st
    #SHEILD Member Involved
    sexecute = "SELECT S.SID, S.SName FROM SHIELDMember S, Participate1 P1 WHERE P1.MID=\'" + MID + "\' AND S.SID = P1.SID" 
    SPs = g.conn.execute(sexecute)
    result = result + "SHIELD Member Involved: "
    for SP in SPs:
      s = str(SP)
      st = "[" + strfun(s) + "]    " + "\r\n"
      result = result + st
    result = result + "--------------- "
    #HYDRA Member Involved
    sexecute = "SELECT H.HID, H.HName FROM HYDRAMember H, Participate2 P2 WHERE P2.MID=\'" + MID + "\' AND H.HID = P2.HID" 
    HPs = g.conn.execute(sexecute)
    result = result + "HYDRA Member Involved: "
    for HP in HPs:
      s = str(HP)
      st = "[" + strfun(s) + "]    " + "\n\r"
      result = result + st
    result = result + "--------------- "
    return result
  except Exception, e:
    print traceback.print_exc()
    return '1'

#Search for ValuableItem
@app.route('/SearchVI')
def SearchVI():
  try:
    VID = str(request.args.get('VID'))
    VName = str(request.args.get('VName'))
    result = ""
    if len(VID) == 0:
      sexecute = "SELECT V.VID FROM ValuableItem V WHERE V.VName=\'" + VName + "\'"
      profiles = g.conn.execute(sexecute)
      for profile in profiles:
        VID = str(profile)
        VID = strfun(VID)
      VID = VID[0: len(VID) - 1]

    #profile
    sexecute = "SELECT V.VID, V.VName, V.VFunction  FROM ValuableItem V WHERE V.VID=\'" + VID + "\'"
    profiles = g.conn.execute(sexecute)
    for profile in profiles:
      s = str(profile)
      st = "Profile: [" + strfun(s) + "]------------- " + "\n"
      result = result + st
    #Mission
    sexecute = "SELECT M.MID, M.MName FROM Mission M, Appearance A WHERE A.VID=\'" + VID + "\' AND M.MID = A.MID" 
    Mis = g.conn.execute(sexecute)
    result = result + "Mission: "
    for Mi in Mis:
      s = str(Mi)
      st = "[" + strfun(s) + "]    " + "\r\n"
      result = result + st
    result = result + "--------------- "

    return result
  except Exception, e:
    print traceback.print_exc()
    return '1'





def querysql(sql):
  cursor = g.conn.execute(sql)
  return cursor

def strfun(s):
  l = len(s)
  s2 = s[2:(l - 1)]
  s2 = string.replace(s2, "u\'","")
  s2 = string.replace(s2, "\'","")
  return s2



"""
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
"""




############################--------- end ----------#####################








#Maybe I should not change these lines

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
