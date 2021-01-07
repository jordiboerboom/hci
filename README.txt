HCI Assignment Team2: Jordi Boerboom, Martine Hazelbag.

makkelijk testen:

Installeer python3
open windows powershell
run pip3 install flask
voer uit: python3 run.py
ga in browser naar localhost:5000

of alternatief voor hosten(windows):
Installeer python3
open windows powershell
run pip3 install flask
run $env:FLASK_APP="run.py"
port forward a port (runs default on port 5000, can be changed in run.py though)
run cmd -> ipconfig -> find local ipv4
run flask run -h <local ip>