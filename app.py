from flask import Flask, request, render_template
import todos
import statuscode
from validator import validate_todo_error,ValidateError
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "secret key boleh random"
jwt = JWTManager(app)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/openapi.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

@app.get('/docs')
def docs():
    return render_template('swagger.html')


# Contoh endpoint untuk login
@app.route("/login", methods=["POST"])
def login():
    # Lakukan validasi username dan password
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    # HTNT: BIkin fungsi buat mengambil data user dari database
    # Dengan menyiapkan 2 parameter di fungsinya yaitu username dan password
    # Dan tabel user harus ada di database(postgres) dengan minimal kolom username dan password
    # if !db.get_user(username, password):
    #     return {"msg": "Username atau password salah"}, 401
    if username != "admin" or password != "admin":
        return {"msg": "Username atau password salah"}, 401

    # Jika validasi berhasil, buat access token
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}, 200


# Contoh endpoint yang memerlukan otentikasi
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Mendapatkan identitas user dari token
    current_user = get_jwt_identity()
    return {"logged_in_as": current_user}, 200


@app.get('/todos')
def get_all_todos():
    return todos.get_all_todos()

@app.get('/todos/<int:id>')
def get_by_id(id):
    todo = todos.get_todo_by_id(id)
    if todo is None:
        return "",statuscode.NOT_FOUND
    return todo

@app.post('/todos')
def create_todo():
    try:
        todo = request.form.get("todo")
        is_done = request.form.get("is_done")
        validate_todo_error(todo, is_done)
        todos.create_new_todo(todo, is_done)
        return "", statuscode.CREATED
    except ValidateError as e:
        return str(e), statuscode.UNPROCESSABLE_ENTITY

@app.put('/todos/<int:id>')
def edit_todo(id):
    if todos.get_todo_by_id(id) is None:
        return "",statuscode.NOT_FOUND
    todo = request.form.get('todo')
    todos.update_todo_by_id(id,todo)
    return "",statuscode.OK

@app.delete('/todos/<int:id>')
def delete_todo(id):
    if todos.get_todo_by_id(id) is None:
        return "",statuscode.NOT_FOUND
    todos.delete_todo_by_id(id)
    return "",statuscode.OK




if __name__==('__main__'):
    app.run(debug=True,use_reloader=True,host="0.0.0.0")