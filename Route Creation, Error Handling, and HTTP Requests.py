from flask import Flask, make_response, request

#always start with 'flask --app server --debug run' split the terminal and run 'curl -X GET -i -w '\n' localhost:5000'

#"app" is the naming convention that will be recalled in the @app.route portion
app= Flask(__name__)

# Route for the main index page. When the server is accessed at the root endpoint, 
# it returns a simple string "Hello World".
@app.route("/")
def index():
    return "Hello World"

# Route for "/no_content". This returns a JSON object with a message and a 204 No Content status code.
# This status is typically used when the server successfully processes the request but is not returning any content.
@app.route("/no_content")
def no_content():
    return ({"Message":"No Content Found"},204)

# Route for "/exp". This demonstrates how to create a response explicitly using the make_response function,
# which allows more control over the response object, including setting headers and status codes directly.
@app.route("/exp")
def indext_explicit():
    resp= make_response({"Message":"Hello World"})
    resp.status_code=200
    return resp

# Route for "/data". This endpoint attempts to return data if available and handles exceptions if data is undefined.
# It returns different messages and status codes based on the presence and state of 'data'.
@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

# Route for "/decorator". This endpoint searches for a person by first name using a query parameter 'q'.
# It demonstrates handling of query parameters and basic error handling if the required parameter is not provided.
@app.route("/decorator")
def name_search():
    query = request.args.get('q')
    if not query:
        return {"measage": "Invalid input parameter"}, 422

    for person in data:
        if query.lower() in person ["first_name"].lower():
            return person

        return ({'message':"person not found"}, 404)  

# This route handles a GET request to count the number of items in 'data'.
# It tries to return the count of 'data' if 'data' is defined.
# If 'data' is not defined, it catches a NameError and returns an error message.
@app.route("/count")
def count():
    try:
        return {"data count": len(data)}, 200
    except NameError:
        return {"message": "data not defined"}, 500

# This route retrieves a person by their UUID from the 'data' list.
# It searches each person's 'id' field for the given UUID. 
# If a match is found, that person's data is returned; otherwise, it returns a 'person not found' message.
@app.route("/person/<uuid:id>")
def find_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            return person
    return {"message": "person not found"}, 404

# This route handles the DELETE request for a person by their UUID.
# It iterates over 'data' to find and remove the person with the specified UUID.
# If the person is found and removed, it returns a success message including the UUID.
# If no person with the UUID is found, it returns a 'person not found' message.
@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            data.remove(person)
            return {"message":f"{id}"}, 200
    return {"message": "person not found"}, 404

# This route handles POST requests to add a new person to the 'data' list.
# It attempts to parse the incoming JSON payload from the request.
@app.route("/person", methods=['POST'])
def add_by_uuid():
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    # code to validate new_person ommited
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500
    return {"message": f"{new_person['id']}"}, 200

# This function is a custom error handler for 404 Not Found errors.
# It gets automatically triggered by Flask whenever a 404 error occurs during request processing.
@app.errorhandler(404)
def api_not_found(error):
    return {"message": "API not found"}, 404

# To run the server, use the command line: flask --app server --debug run
# To test the endpoints, use the command line tool 'curl' with appropriate commands.     