# import os
# import mimetypes

# # ---------------------------
# # Exclude specific folders
# # ---------------------------
# SCRIPT_PATH = os.path.abspath(__file__)
# EXCLUDE_DIRS = [
#     os.path.abspath("../runner")  # skip runner folder
# ]

# # ---------------------------
# # Wiping Algorithms
# # ---------------------------
# def simple_wipe(path, passes=1):
#     size = os.path.getsize(path)
#     with open(path, "ba+", buffering=0) as f:
#         for _ in range(passes):
#             f.seek(0)
#             f.write(os.urandom(size))
#             f.flush()
#             os.fsync(f.fileno())
#     os.remove(path)

# def multipass_wipe(path, passes=3):
#     size = os.path.getsize(path)
#     patterns = [b"\x00", b"\xFF", os.urandom(1)]
#     with open(path, "ba+", buffering=0) as f:
#         for i in range(passes):
#             f.seek(0)
#             pat = patterns[i % len(patterns)] * size
#             f.write(pat)
#             f.flush()
#             os.fsync(f.fileno())
#     os.remove(path)

# def gutmann_wipe(path):
#     size = os.path.getsize(path)
#     patterns = [b"\x55", b"\xAA", b"\x92", b"\x49", b"\x24"] + [os.urandom(1)]*5
#     with open(path, "ba+", buffering=0) as f:
#         for pat in patterns:
#             f.seek(0)
#             f.write(pat * size)
#             f.flush()
#             os.fsync(f.fileno())
#     os.remove(path)

# # ---------------------------
# # Recommendation Engine
# # ---------------------------
# def recommend_algo(path, size_threshold=10*1024*1024):
#     mime, _ = mimetypes.guess_type(path)
#     size = os.path.getsize(path)
#     if mime and "text" in mime:
#         if "password" in path.lower() or "config" in path.lower():
#             return "gutmann"
#         return "multipass"
#     if mime and ("image" in mime or "video" in mime):
#         return "simple" if size > size_threshold else "multipass"
#     if mime and "pdf" in mime:
#         return "multipass"
#     return "simple"

# # ---------------------------
# # Wipe Directory
# # ---------------------------
# import shutil

# def wipe_directory(root="."):
#     root = os.path.abspath(root)

#     # 1️⃣ Wipe all files
#     for dirpath, _, filenames in os.walk(root):
#         dirpath_abs = os.path.abspath(dirpath)
#         if any(dirpath_abs.startswith(d) for d in EXCLUDE_DIRS):
#             continue
#         for file in filenames:
#             path = os.path.join(dirpath, file)
#             if "__pycache__" in path:
#                 continue
#             algo = recommend_algo(path)
#             if algo == "simple":
#                 simple_wipe(path)
#             elif algo == "multipass":
#                 multipass_wipe(path)
#             elif algo == "gutmann":
#                 gutmann_wipe(path)

#     # 2️⃣ Remove __pycache__ folders inside root
#     for dirpath, dirnames, _ in os.walk(root, topdown=False):
#         for d in dirnames:
#             if d == "__pycache__":
#                 pycache_path = os.path.join(dirpath, d)
#                 shutil.rmtree(pycache_path, ignore_errors=True)

#     # 3️⃣ Remove root wiping folder itself
#     if os.path.exists(root):
#         shutil.rmtree(root, ignore_errors=True)
#         print(f"[i] Wiping folder {root} deleted successfully.")

import os
import shutil
import mimetypes

# ---------------------------
# Exclude runner folder
# ---------------------------
EXCLUDE_DIRS = [
    os.path.abspath("../runner")
]

# ---------------------------
# Wiping Algorithms
# ---------------------------
def simple_wipe(path, passes=1):
    size = os.path.getsize(path)
    with open(path, "ba+", buffering=0) as f:
        for _ in range(passes):
            f.seek(0)
            f.write(os.urandom(size))
            f.flush()
            os.fsync(f.fileno())
    os.remove(path)

def multipass_wipe(path, passes=3):
    size = os.path.getsize(path)
    patterns = [b"\x00", b"\xFF", os.urandom(1)]
    with open(path, "ba+", buffering=0) as f:
        for i in range(passes):
            f.seek(0)
            pat = patterns[i % len(patterns)] * size
            f.write(pat)
            f.flush()
            os.fsync(f.fileno())
    os.remove(path)

def gutmann_wipe(path):
    size = os.path.getsize(path)
    patterns = [b"\x55", b"\xAA", b"\x92", b"\x49", b"\x24"] + [os.urandom(1)]*5
    with open(path, "ba+", buffering=0) as f:
        for pat in patterns:
            f.seek(0)
            f.write(pat * size)
            f.flush()
            os.fsync(f.fileno())
    os.remove(path)

# ---------------------------
# Algorithm Recommendation
# ---------------------------
def recommend_algo(path, size_threshold=10*1024*1024):
    mime, _ = mimetypes.guess_type(path)
    size = os.path.getsize(path)
    if mime and "text" in mime:
        if "password" in path.lower() or "config" in path.lower():
            return "gutmann"
        return "multipass"
    if mime and ("image" in mime or "video" in mime):
        return "simple" if size > size_threshold else "multipass"
    if mime and "pdf" in mime:
        return "multipass"
    return "simple"

# ---------------------------
# Wipe Directory
# ---------------------------
def wipe_directory(root="../wiping"):
    root = os.path.abspath(root)

    # 1️⃣ Wipe all files
    for dirpath, _, filenames in os.walk(root):
        dirpath_abs = os.path.abspath(dirpath)
        if any(dirpath_abs.startswith(d) for d in EXCLUDE_DIRS):
            continue
        for file in filenames:
            path = os.path.join(dirpath, file)
            if "__pycache__" in path:
                continue
            algo = recommend_algo(path)
            if algo == "simple":
                simple_wipe(path)
            elif algo == "multipass":
                multipass_wipe(path)
            elif algo == "gutmann":
                gutmann_wipe(path)

    # 2️⃣ Remove __pycache__ folders
    for dirpath, dirnames, _ in os.walk(root, topdown=False):
        for d in dirnames:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(dirpath, d), ignore_errors=True)

    # 3️⃣ Remove the root wiping folder
    if os.path.exists(root):
        shutil.rmtree(root, ignore_errors=True)
        print(f"[i] Wiping folder {root} deleted successfully.")
