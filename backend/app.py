from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from extensions import db, bcrypt, jwt
from models import User, Task

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_manager.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "change-this-secret"  # coloca algo mais seguro

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    # ---------- Public Routes ----------

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"msg": "Missing data"}), 400

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return jsonify({"msg": "User already exists"}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    # ---------- Private Routes (TASKS) ----------

    @app.route("/tasks", methods=["GET"])
    @jwt_required()
    def get_tasks():
        current_user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        return jsonify([
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "done": t.done,
                "category": t.category, 
            } for t in tasks
        ])

    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def create_task():
        current_user_id = get_jwt_identity()
        data = request.get_json()
        title = data.get("title")
        description = data.get("description", "")
        category = data.get("category", "personal")

        if not title:
            return jsonify({"msg": "Title is required"}), 400

        allowed_categories = {"work", "study", "personal", "other"}
        if category not in allowed_categories:
            category = "other"


        task = Task(title=title, description=description, category=category, user_id=current_user_id)
        db.session.add(task)
        db.session.commit()

        return jsonify({"msg": "Task created", "id": task.id}), 201

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    @jwt_required()
    def update_task(task_id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        if task is None:
            return jsonify({"msg": "Task not found"}), 404

        data = request.get_json()
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.done = data.get("done", task.done)

        category = data.get("category", task.category)
        allowed_categories = {"work", "study", "personal", "other"}
        if category in allowed_categories:
            task.category = category
            
        db.session.commit()

        return jsonify({"msg": "Task updated"})

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    @jwt_required()
    def delete_task(task_id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        if task is None:
            return jsonify({"msg": "Task not found"}), 404

        db.session.delete(task)
        db.session.commit()
        return jsonify({"msg": "Task deleted"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
