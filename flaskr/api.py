import psycopg2
from flask import Blueprint, request
from . import db

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route("/resources/users", methods=["POST"])
def add_user():
    conn = db.get_conn()
    cursor = conn.cursor()

    body = request.json
    if validate_user_data(body):
        user = body["user"]
    else:
        return {"error": {"msg": "Input is invalid."}}, 400

    try:
        cursor.execute("""
                        INSERT INTO users (email, password, first_name, last_name)
                        VALUES (%s, %s, %s, %s)
                        RETURNING user_id, email, password, first_name, last_name;
                        """,
                       (user["email"], user["password"], user["firstName"], user["lastName"]))
        conn.commit()
    except psycopg2.Error as error:
        return {"error": {"msg": str(error)}}, 400

    result = cursor.fetchone()

    cursor.close()

    return {
        "result": {
            "id": result[0],
            "email": result[1],
            "password": result[2],
            "firstName": result[3],
            "lastName": result[4],
        }
    }


def validate_user_data(user_data) -> bool:
    if type(user_data) is not dict:
        return False

    user = user_data.get("user")
    if not user:
        return False

    required_fields = ["email", "password", "firstName", "lastName"]
    for field in required_fields:
        field_value = user.get(field)
        if not field_value or type(field_value) is not str:
            return False

    return True


@bp.route("/resources/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return {"error": {"msg": "User id is invalid."}}, 400

    conn = db.get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                        SELECT user_id, email, first_name, last_name
                        FROM users
                        WHERE user_id = %s;
                        """,
                       (user_id,))

        user = cursor.fetchone()
    except psycopg2.Error as error:
        return {"error": {"msg": str(error)}}, 400

    cursor.close()

    if user:
        return {
            "result": {
                "id": user[0],
                "email": user[1],
                "firstName": user[2],
                "lastName": user[3],
            }
        }
    else:
        return {"error": {"msg": f"Could not find a user with ID {user_id}."}}, 400


@bp.route("/resources/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return {"error": {"msg": "User id is invalid."}}, 400

    conn = db.get_conn()
    cursor = conn.cursor()

    body = request.json
    if validate_user_data(body):
        user = body["user"]
    else:
        return {"error": {"msg": "Input is invalid."}}, 400

    try:
        cursor.execute("""
                        UPDATE users
                        SET email = %s, password = %s, first_name = %s, last_name = %s
                        WHERE user_id = %s
                        RETURNING user_id, email, password, first_name, last_name;
                        """,
                       (user["email"], user["password"], user["firstName"], user["lastName"], user_id))
        conn.commit()
    except psycopg2.Error as error:
        return {"error": {"msg": str(error)}}, 400

    result = cursor.fetchone()

    cursor.close()

    return {
        "result": {
            "id": result[0],
            "email": result[1],
            "password": result[2],
            "firstName": result[3],
            "lastName": result[4],
        }
    }
