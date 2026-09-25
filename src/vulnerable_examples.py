import ast
import json
import os
import sqlite3

import tarfile
from django.utils.html import escape

SECRET_KEY = os.environ.get("SECRET_KEY", "default-fallback-key-for-dev-only")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1")


def search_safe(request, MyModel):
    q = request.GET.get("q", "")
    rows = MyModel.objects.filter(name__icontains=q)
    return rows


def save_comment_safe(request, CommentModel):
    user_input = request.POST.get("comment", "")
    comment = CommentModel()
    comment.html = escape(user_input)
    comment.save()
    return comment


def backup_safe(request):
    filename = request.GET.get("file", "")

    if not filename or ".." in filename or "/" in filename or "\\" in filename:
        return "invalid filename"

    src_path = f"/data/{filename}"
    archive_path = f"/backup/{filename}.tar.gz"

    if not os.path.exists(src_path):
        return "file not found"

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(src_path, arcname=filename)
    except Exception:
        return "backup failed", 500

    return "ok"


def load_object_safe(uploaded_file):
    data = uploaded_file.read()
    obj = json.loads(data.decode("utf-8"))
    return obj


def update_profile_safe(request):
    return "profile updated"


def get_user_data_safe(username):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchall()
    db.close()
    return user_data


def calculate_expression(expression):
    """
    Безпечно обчислює тільки базові математичні/літеральні вирази.
    """
    try:
        result = ast.literal_eval(expression)
        print(f"Результат: {result}")
        return result
    except (ValueError, SyntaxError) as e:
        print(f"Помилка некоректного виразу: {e}")
        return None

calculate_expression("2 + 3 * 4")

def run_user_expression():
    user_input = input("Enter math expression: ")
    result = calculate_expression(user_input)
    print("Result:", result)
