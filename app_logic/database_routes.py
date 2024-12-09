from datetime import datetime, timezone
from flask import jsonify, request, current_app, session
from app_logic.models import PlayerScore, User
from app_logic.database import db, init_db_connection, load_sql_queries
from werkzeug.security import generate_password_hash, check_password_hash

# ==============================
# API ENDPOINTS
# ==============================


def fetch_leaderboard():
    """
    Retrieve the leaderboard.
    - Fetches the top 10 players based on the shortest completion time.
    - Players are ranked in ascending order of their completion time.

    Returns:
        JSON list of player scores (top 10).
    """
    try:
        scores = (
            PlayerScore.query.order_by(PlayerScore.completion_time.asc())
            .limit(10)
            .all()
        )
        return jsonify([score.to_dict() for score in scores]), 200
    except Exception as e:
        return jsonify(
            {"error": f"Failed to fetch leaderboard: {str(e)}"}
        ), 500


def submit_score():
    """
    Submit a player's score.
    Accepts player data (name, completion time, and number of moves) as JSON input.

    Request Body:
        {
            "player_name": "John",
            "completion_time": 45.5,
            "moves": 20
        }

    Returns:
        The saved player score in JSON format.
    """
    data = request.get_json()
    player_name = data.get("player_name")
    completion_time = data.get("completion_time")
    moves = data.get("moves")

    # Validate input data
    if (
        not player_name
        or not isinstance(completion_time, (int, float))
        or not isinstance(moves, int)
    ):
        return jsonify(
            {
                "error": "Invalid data: Ensure player_name is a string, "
                "completion_time is a number, and moves is an integer."
            }
        ), 400

    return internal_submit_score(player_name, completion_time, moves)


def internal_submit_score(player_name, completion_time, moves):
    """
    Internal helper function to insert the player's score into the database.
    """
    try:
        score = PlayerScore(
            player_name=player_name,
            completion_time=float(completion_time),
            moves=moves,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(score)
        db.session.commit()
        return jsonify(score.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to submit score: {str(e)}"}), 500


def check_player():
    """
    Check if a player is already registered.
    Accepts a 'player_name' as a query parameter.

    Query Parameters:
        player_name (str): The name of the player to check.

    Returns:
        "True" if the player exists, "False" otherwise.
    """
    player_name = request.args.get("player_name", default=None, type=str)

    if not player_name:
        return "False", 400

    try:
        exists = (
            PlayerScore.query.filter_by(player_name=player_name).first()
            is not None
        )
        return str(exists), 200
    except Exception as e:
        print(f"Error checking player: {e}")
        return "False", 500


def check_player_existence(player_name):
    """
    Internal helper function to check if a player already exists.
    Replicates the logic of the check_player endpoint, but works internally.
    """
    if not player_name:
        return False

    try:
        exists = (
            PlayerScore.query.filter_by(player_name=player_name).first()
            is not None
        )
        return exists
    except Exception as e:
        print(f"Error checking player internally: {e}")
        return False


def init_tables():
    """
    Check if 'player_scores' and 'users' tables exist in the database.
    If they do not exist, create them using SQL statements from sql_queries.ini.
    This can be called at the start of the game to ensure tables are created.
    """
    queries = load_sql_queries("sql_queries.ini")
    db_url = current_app.config.get("DB_URL")
    if not db_url:
        return jsonify(
            {"error": "Database URL (DB_URL) is not configured."}
        ), 500

    try:
        conn, cur = init_db_connection(db_url)

        # Check 'player_scores' table
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'player_scores'
            );
        """)
        player_scores_exists = cur.fetchone()[0]

        # Check 'users' table
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        users_exists = cur.fetchone()[0]

        # Create 'player_scores' if not exists
        if not player_scores_exists:
            create_player_scores_sql = queries.get(
                "table_creation", "create_player_scores"
            )
            cur.execute(create_player_scores_sql)
            conn.commit()

        # Create 'users' if not exists
        if not users_exists:
            create_users_sql = queries.get("table_creation", "create_users")
            cur.execute(create_users_sql)
            conn.commit()

        cur.close()
        conn.close()

        return jsonify(
            {
                "message": "Tables checked and created if they did not exist.",
                "player_scores_existed": player_scores_exists,
                "users_existed": users_exists,
            }
        ), 200

    except Exception as e:
        return jsonify(
            {"error": f"Failed to initialize tables: {str(e)}"}
        ), 500


def register():
    """
    Register a new user.
    Expects JSON: {"username": "John", "password": "example123"}
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists."}), 400

    new_user = User(username=username)
    new_user.password_hash = generate_password_hash(password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to register user: {str(e)}"}), 500


def login():
    """
    User login.
    Expects JSON: {"username": "John", "password": "example123"}
    On success, sets session state 'logged_in' and stores the 'username'.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session["logged_in"] = True
        session["username"] = username
        return jsonify({"message": "Login successful."}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401


def logout():
    """
    User logout.
    Clears the session.
    """
    session.clear()
    return jsonify({"message": "Logged out successfully."}), 200
