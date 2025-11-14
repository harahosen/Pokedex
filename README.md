# Pokedex API

This is a simple implementation for a Pokedex API with two endpoints:

1. One for basic pokemon info taken from [PokeAPI](https://pokeapi.co/)
2. One for a translated description of a pokemon taken from [Funtranslations](https://funtranslations.com/)


## Premise

Despite my past professional experience with other languages, this is my first web project with Python - and I loved it! After having desingned the basic structure, I used some AI tools mostly as assistance or the use of the libraries needed, like FastAPI and Pytest. I took the project as an opportunity to learn, and I had fun with it. :)

## Repo contents

### Structure

Inside the "app" folder there is all the logic:
- main.py: generic orchestrator
- routes/pokemon.py: endpoint definitions
- services: communication handling with the external APIs
- exceptions/handlers: error management
- utils: utility files

### Tests

The app will run without these files, but I included a bunch of tests I put in place with Pytest. They are marked with the following tags:
- unit
- schema
- integration
- smoke
- e2e

In this way they could be run by tag, e.g.: ```python -m pytest -m integration```

### Misc files

Utility files for the app installation, git, Docker configuration... this kind of things

## Basic configuration

In order to use the app, be sure to have [Git](https://git-scm.com/install) and [Python](https://www.python.org/downloads/) installed (I used Python 3.13). Now you should be able to clone the repo. Now there are two possible ways to continue:

a) Run everything on local, following these steps on a terminal or with the IDE of your preference:
  1. Inside of your local folder, create a virtual environment: ```python3.13 -m venv venv``` (use another recent Python version, eventually)
  2. Activate a virtual environent: ```.venv\Scripts\activate```
  3. Install the needed dependencies (the file is included in the repo): ```pip install -r requirements.txt```
  4. Run uvicorn (be sure to be inside the "app" directory): ```uvicorn main:app --reload --host 0.0.0.0 --port 8000```
  5. Now you should be able to use the app on local on the port 8000; to access it, you can click on the link provided by uvicorn, use curl or a tool [HTTPie](https://httpie.io/app) (n.b.: you will need the [desktop app](https://httpie.io/download) to use it on local)
  6. Modify the URL with the wanted endpoint, adding "/pokemon/<pokemon name>" for the basic info or "/pokemon/translated/<pokemon name>" for the version with the translated description
 
b) Use Docker. The simplest way to install it with [Docker Desktop](https://www.docker.com/get-started/):
  1. Open Docker Desktop
  2. Run the command inside the directory you saved the repo: ```docker build -t pokedeximage .```
  3. Run the command: ```docker run -d -p 8000:8000 --name pokedex pokedeximage``` - you can use different ports and container name
  4. Now you should be able to test the endpoints with curl: ```curl http://localhost:8000/pokemon/<pokemon name>``` or ```curl http://localhost:8000/pokemon/translated/<pokemon name>```
  5. Stop the container: ```docker stop pokedex```
  6. Delete the container: ```docker rm pokedex```
  7. Remove the image: ```docker rmi pokedeximage```

If you prefer to work with a GUI, instead of running the commands from point 3, you can proceed with these steps on Docker Desktop:
  1. Inside the "Images" section of Docker Desktop, you should be able to see one image named "pokedeximage" (n.b.: this is created by the dockerfile inside the repo: it has a bunch of pre-compiled section, like the system image of a light OS with Python 3.13, the switching to a not-root user and the use o the port 8000; you can edit the file if you prefer to have a different configuration)
  2. Clik on the "Run" button
  3. Open the "Optional settings" and on the "Host port" tab assign a preferred one (or write 0 if you want to use a random one)
  4. Under the container name and the container ID, you should be able to see a clickable link
  5. Modify the URL with the wanted endpoint, adding "/pokemon/<pokemon name>" for the basic info or "/pokemon/translated/<pokemon name>" for the version with the translated description
  6. You can stop and delte the container using the dedicate buttons
  7. In a similar way, you can delete the image
 
 
The final output should be something similar to these (first one created using the clickable URL, second one using curl inside the terminal):

1. Using the clickable link:
```
name	"abra"
description	"Using its ability to read minds, it will identify impending danger and TELEPORT to safety."
habitat	"urban"
isLegendary	false
```

2. Using curl:
```
StatusCode        : 200
StatusDescription : OK
Content           : {"name":"ditto","description":"Capable of copying an enemy's genetic code to instantly transform itself into a duplicate of the enemy.","habitat":"urban","isLegendary":false}
RawContent        : HTTP/1.1 200 OK
                    Content-Length: 174
                    Content-Type: application/json
                    Date: Fri, 14 Nov 2025 09:12:37 GMT
                    Server: uvicorn
                    {"name":"ditto","description":"Capable of copying an enemy's genetic code ...
Forms             : {}
Headers           : {[Content-Length, 174], [Content-Type, application/json], [Date, Fri, 14 Nov 2025 09:12:37 GMT], [Server, uvicorn]}       
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 174
```


## Considerations before going on PROD

This app is a simple POC: I tried to keep a clean and minimal architecture, but it is not production-ready. I will list here some possible improvements, but some of them could vary depending on the business needs.

### Security

There is no authentication for the app, while in a production-environment would probably need some kind of authorization.

### Caching

There is no specific caching at the moment. In a first phase, it would be helpful at least a basic form of caching, leaving place for a more refined system in eventual future developments based on the scaling needs.

### Versioning

A proper versioning of the API could be helpful for future feature implementations.

### Robustness and resiliency

A solid product would need a refined system for timeouts and retries, with the implementation of a rate limiter and eventually a load balancer. 

### Testing

As written before, this is a simple POC. A complete product will need more specific tests than the ones I did, like performance and load tests. Moreover, accordingly with the business, some feature could be added, so a battery of acceptance tests would be needed (and consequently new unit an integration tests).
