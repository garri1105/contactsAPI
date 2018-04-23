# contactsAPI

Developed as a 72 hour project for Inkit.io

This project uses Python 3.6 and it's compatible with Python 2.7 but more testing is necessary to ensure compatibility.

## Get Started

After you clone this repository,
```git clone https://github.com/Garri1105/contactsAPI```


the first step to run the API will be creating a Python virtual environment.
```
$ cd contactsAPI
$ virtualenv .venv
$ source .venv/bin/activate
```
or if you are on windows.
```
$ source .venv/Scripts/activate
```


Install all the required Python packages
```
pip install -r requirements.txt
```

Finally initialize the server in http://localhost:8000,
```
waitress-serve --port=8000 inkit_project:app.app
```


You should be now be able to send requests to the API. All the information is stored in ```contacts.db``` in your root folder. 
