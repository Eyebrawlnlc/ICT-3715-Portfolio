import os

for root, dirs, files in os.walk(r"C:\Users\nisha"):
    for f in files:
        if "amandla" in f.lower() and f.endswith(".sql"):
            print("FOUND:", os.path.join(root, f))