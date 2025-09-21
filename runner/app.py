# from flask import Flask, render_template, request
# import os
# import sys

# # Add wiping folder to Python path
# sys.path.append("../wiping")
# from wipe_all import wipe_directory, recommend_algo

# app = Flask(__name__)
# FOLDER_TO_WIPE = "../wiping"  # Only target wiping folder

# # Helper to list files
# def list_files(root):
#     file_list = []
#     for dirpath, _, filenames in os.walk(root):
#         for f in filenames:
#             path = os.path.join(dirpath, f)
#             rel_path = os.path.relpath(path, root)
#             algo = recommend_algo(path)
#             file_list.append({"path": rel_path, "algo": algo})
#     return file_list

# @app.route("/", methods=["GET"])
# def index():
#     files = list_files(FOLDER_TO_WIPE)
#     return render_template("index.html", files=files)

# @app.route("/wipe", methods=["POST"])
# def wipe():
#     for rel_path, algo_choice in request.form.items():
#         path = os.path.join(FOLDER_TO_WIPE, rel_path)
#         if not os.path.isfile(path):
#             continue
#         # Apply selected algorithm
#         from wipe_all import simple_wipe, multipass_wipe, gutmann_wipe
#         if algo_choice == "simple":
#             simple_wipe(path)
#         elif algo_choice == "multipass":
#             multipass_wipe(path)
#         elif algo_choice == "gutmann":
#             gutmann_wipe(path)
#     return "<h2>Wipe Completed!</h2><a href='/'>Go back</a>"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)

from flask import Flask, render_template, request
import os
import sys

# Add wiping folder to Python path
sys.path.append("../wiping")
from wipe_all import wipe_directory, recommend_algo, simple_wipe, multipass_wipe, gutmann_wipe

app = Flask(__name__)
FOLDER_TO_WIPE = "../wiping"  # Only target wiping folder

# List all files for UI
def list_files(root):
    file_list = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(path, root)
            algo = recommend_algo(path)
            file_list.append({"path": rel_path, "algo": algo})
    return file_list

@app.route("/", methods=["GET"])
def index():
    files = list_files(FOLDER_TO_WIPE)
    return render_template("index.html", files=files)

@app.route("/wipe", methods=["POST"])
def wipe():
    # Apply selected algorithm for each file
    for rel_path, algo_choice in request.form.items():
        path = os.path.join(FOLDER_TO_WIPE, rel_path)
        if not os.path.isfile(path):
            continue
        if algo_choice == "simple":
            simple_wipe(path)
        elif algo_choice == "multipass":
            multipass_wipe(path)
        elif algo_choice == "gutmann":
            gutmann_wipe(path)

    # Remove empty directories + __pycache__ + wiping folder itself
    wipe_directory(FOLDER_TO_WIPE)
    return "<h2>Wipe Completed!</h2><a href='/'>Go back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
