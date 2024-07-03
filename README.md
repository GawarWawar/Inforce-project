Not usable at the moment, but with some fixes can be very useful: 
1. Build docker container:  
docker build .
2. Run docker container:
docker run container_id

TODO: fix docker having problems with building (because of psycorg2) and connecting to the DB  

Prefereble way for now to launch the app:  
1. Start postgres server;
1.5 Install all reuirements:
$ python3 -m pip install -r requirements.txt
2. Use comand to migrate all data:
$ python3 manage.py migrate

Shared steps:  
3. Create superuser:  
$ python3 manage.py createsuperuser  
4. Server should be avaible at 0.0.0.0:8000;
5. In test_endpoints.rest - there is manual starter of every endpoint avaible;
6. In every urls.py - brief explanation of what endpoint does; doesnt specify return type or form;
7. All Models can be used in Admin. However, there are not configured fully

A little bit more about endpoints:
- main endpoints, that were given as a main exercise, are located at the top of api_server.urls;  
- At the bottom - additional endpoints that were created to give more broad functionality to app. However, later it became clear, that they are redundunt for now. But they were already implimented, so they were left in app.  

About future TODOs:  
- add proper docks; 
- add tests;
- vrappers, that are located in data_management, should be done as classes, to ensure more broad and easier usage;  
- all endpoints that use @api_view - should be remake into classes for the same reason;  
As a side NOTE, functions were used as a starter, however time was closing too quickly, so they were left as a concept.
- impliment expiration time/date for teh tokens.