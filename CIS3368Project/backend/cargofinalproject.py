import hashlib
import flask
from flask import jsonify
from flask import request, make_response

from sqlconnector import create_connection
from sqlconnector import execute_read_query
from sqlconnector import execute_query

import credentials

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create connection to MySQL database
myCreds = credentials.Creds()
connection = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)

masterUsername = "username"
masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

# Login API
@app.route('/authenticatedroute', methods=['GET'])
def TestAuthorization():
    if request.authorization:
        encoded = request.authorization.password.encode() 
        hasedResult = hashlib.sha256(encoded) 
        if (request.authorization.username == masterUsername) and (hasedResult.hexdigest() == masterPassword):
            return make_response('Authorized', 200)
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

# GET Cargo Functionality
@app.route('/api/cargo/all', methods=['GET'])
def GETcargo():
    sql = 'SELECT * FROM cargo'
    cargo = execute_read_query(connection, sql)
    return jsonify(cargo)

# POST Cargo Functionality
@app.route('/api/cargo', methods=['POST'])
def POSTcargo():
    
    request_data = request.get_json()
    uWeight = int(request_data['weight'])
    uCargotype = request_data['cargotype']
    uDeparture = request_data['departure']
    uArrival = request_data['arrival']
    uShipID = int(request_data['shipid'])

    # cursor = connection.cursor()

    # Grabbing the maxweight and weight of the spaceship
    capacity_sql = "SELECT maxweight FROM spaceship WHERE id = %d" % (uShipID)
    maxcapacity_result = execute_read_query(connection, capacity_sql)
    maxcapacity = maxcapacity_result[0].get('maxweight')

    weight_sql = "SELECT SUM(weight) AS sum FROM cargo WHERE shipid = %d" % (uShipID)
    loaded_weight_result = execute_read_query(connection, weight_sql)
    loaded_weight = loaded_weight_result[0].get('sum')

    # Check if there is enough space on the spaceship
    if (loaded_weight + uWeight) <= maxcapacity:
        # Add the cargo to the database
        sql = "INSERT INTO cargo(weight, cargotype, departure, arrival, shipid) VALUES (%d, '%s', '%s', '%s', %d)" % (uWeight, uCargotype, uDeparture, uArrival, uShipID)
        execute_query(connection, sql)
        return 'Data insertion completed!', 200
    else:
        return 'Not enough space on the spaceship!', 400

# DELETE Cargo Functionality
@app.route('/api/cargo', methods=['DELETE'])
def DELETEcargo():
    request_data = request.args.get('id')
    idtodelete = int(request_data)
    
    sql = "delete from cargo where id = %d" % (idtodelete)
    execute_query(connection, sql)
        
    return "Delete request successful!"

# UPDATE Cargo Functionality
@app.route('/api/cargo', methods=['PUT'])
def PUTcargo():
        request_data = request.get_json()
        sql = "update cargo set weight = %d, cargotype = '%s', departure = '%s', arrival = '%s', shipid = %d where id = %d" % (int(request_data['weight']), request_data['cargotype'], request_data['departure'], request_data['arrival'], int(request_data['shipid']), int(request_data['id']))
        execute_query(connection, sql)
        return 'Update request successful!'

# GET Spaceship Functionality
@app.route('/api/spaceship/all', methods=['GET'])
def GETspaceship():
    sql = 'SELECT * FROM spaceship'
    spaceship = execute_read_query(connection, sql)
    return jsonify(spaceship)

# POST Spaceship Functinality
@app.route('/api/spaceship', methods=['POST'])
def POSTspaceship():
    request_data = request.get_json()
    uMaxweight = int(request_data['maxweight'])
    uCaptainID = int(request_data['captainid'])

    sql = "INSERT INTO spaceship(maxweight, captainid) VALUES (%d, %d)" % (uMaxweight, uCaptainID)
    execute_query(connection, sql)
    return 'Data insertion completed!'

# DELETE Spaceship Functionality
@app.route('/api/spaceship', methods=['DELETE'])
def DELETEspacehsip():
    request_data = request.args.get('id')
    idtodelete = int(request_data)
    
    sql = "delete from spaceship where id = %d" % (idtodelete)
    execute_query(connection, sql)
        
    return "Delete request successful!"

# UPDATE Spaceship Functionality
@app.route('/api/spaceship', methods=['PUT'])
def PUTspaceship():
        request_data = request.get_json()
        sql = "update spaceship set maxweight = %d, captainid = %d where id = %d" % (int(request_data['maxweight']), int(request_data['captainid']), int(request_data['id']))
        execute_query(connection, sql)
        return 'Update request successfull'

# GET Captain Functionality
@app.route('/api/captain/all', methods=['GET'])
def GETcaptain():
    sql = 'SELECT * FROM captain'
    captain = execute_read_query(connection, sql)
    return jsonify(captain)

# POST Captain Functionality
@app.route('/api/captain', methods=['POST'])
def POSTcaptain():
    request_data = request.get_json()
    uFirstname = request_data['firstname']
    uLastname = request_data['lastname']
    uRank = request_data['rankstatus']
    uHomeplanet = request_data['homeplanet']

    sql = "INSERT INTO captain(firstname, lastname, rankstatus, homeplanet) VALUES ('%s', '%s', '%s', '%s')" % (uFirstname, uLastname, uRank, uHomeplanet)
    execute_query(connection, sql)
    return 'Data insertion completed!'

# DELETE Captain Functionality
@app.route('/api/captain', methods=['DELETE'])
def DELETEcaptain():
    request_data = request.args.get('id')
    idtodelete = int(request_data)
    
    sql = "delete from captain where id = %d" % (idtodelete)
    execute_query(connection, sql)
        
    return "Delete request successful!"

# UPDATE Captain Functionality
@app.route('/api/captain', methods=['PUT'])
def PUTcaptain():
        request_data = request.get_json()
        sql = "update captain set firstname = '%s', lastname = '%s', rankstatus = '%s', homeplanet = '%s' where id = %d" % (request_data['firstname'], request_data['lastname'], request_data['rankstatus'], request_data['homeplanet'], int(request_data['id']))
        execute_query(connection, sql)
        return 'Update request successful'

app.run()
