# peaks_api 
## Presentation
peaks_api is a API managing some mountain's peaks data in a datastore.<br/>
### Tools
The project is a developpement phase, deployed in a composition of containers using Docker.<br/>
Backend code is python 3.9.4, with (but not limited to):<br/>
- FastAPI for the API itself.<br/>
- orma for the ORM model.<br/>
- PostgreSQL for the database.<br/>
- traefik for the load balancer.<br/>
### Developpement
All the developpement was performed on Windows in WSL2, so the project is expected to work under linux or MAC.<br/>
Note that .devcontainer folder is specific to Visual Studio Code, to build and to open containers in the IDE, and therefore is not required to run the application itself.<br/> 
## How to
To launch the application: <br/>
- Clone the repository.<br/>
- Launch the docker compose => docker-compose up -d<br/>
- Go to http://fastapi.localhost:8008/ and http://fastapi.localhost:8081/dashboard/#/ to see the result.<br/>
peaks are available under /peaks route, where you can manage them: get/add/update/delete peaks (partial update is possible).<br/>
Note that the datastore is at first empty, but as an exemple, you can add your first peak with the following payload:<br/>
{"name": "Mont Blanc",<br/> 
 "alt" : 4808,<br/>
 "lat" : 45.832622,<br/>
 "lon" : 6.865175}<br/>
Once you added some peaks, you can use the /peaks/search/ route to filter peaks by name:<br/>
http://fastapi.localhost:8008/search/?name=Mont Blanc<br/>
or by match a (lat_min, lat_max, lon_min, lon_max) box:<br/>
http://fastapi.localhost:8008/peaks/search/?lat_min=0&lat_max=50&lon_min=-45&lon_max=5<br/>

Also note that some unittest are available in tests folder, and must be executed first and foremost any action with the API ; otherwise some of the tests will fail due to some static choice for this version,and you will have to put down and up the container to clear the datastore.<br/>
