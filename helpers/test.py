import json

string = "{3: {'id': '1', 'first_name': 'Jermayne', 'last_name': 'Stevings', 'email': 'jstevings0@time.com', 'gender': 'Male', 'ip_address': '126.144.109.82', }, 1: {'id': '3', 'first_name': 'Tildy', 'last_name': 'Guiso', 'email': 'tguiso2@wix.com', 'gender': 'Female', 'ip_address': '235.113.1.92', }, 2: {'id': '7', 'first_name': 'Courtney', 'last_name': 'Swainger', 'email': 'cswainger6@nbcnews.com', 'gender': 'Female', 'ip_address': '120.31.214.140', }, 3: {'id': '8', 'first_name': 'Jodi', 'last_name': 'O'Carroll', 'email': 'jocarroll7@springer.com', 'gender': 'Female', 'ip_address': '92.48.44.22', }, 4: {'id': '9', 'first_name': 'Katusha', 'last_name': 'Greenough', 'email': 'kgreenough8@last.fm', 'gender': 'Female', 'ip_address': '71.223.55.209', }}"

data = json.loads(string)
