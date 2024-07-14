import os
import csv
import sys

directory = "../by-contestant"

data = []

for filename in sorted(os.listdir(directory)):
    file_parts = filename.split(" - ")
    if len(file_parts) >= 2:
        username = file_parts[0].strip()
        name = file_parts[1].strip()
        name = " ".join(name.split(" ")[:-1])
        email = username + "@toki.id"
        password = "puspresnas"
        data.append([username, name, email, password])

writer = csv.writer(sys.stdout)
writer.writerow(["username", "name", "email", "password"])
writer.writerows(data)
