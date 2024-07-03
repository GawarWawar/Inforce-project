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
- 1st and 2nd endpoints in test_endpoints.rest (signup and login) - doesnt require token. Every other endpoint does. From both of signup and login tokens -> access can be obtained to get access to other endpoints;
- Some endpoints require admin permisions. Using login with {"username": "name_of_SUPERuser", "password": "password_for_SUPERuser" } - admin token can be obtained. To change user to admin, PUT api/users/<user_id> can be used;
- main endpoints, that were given as a main exercise, are located at the top of api_server.urls and they will be listed at the end of README;  
- At the bottom - additional endpoints that were created to give more broad functionality to app. However, later it became clear, that they are dont represent functions from the exercise, therefore redundunt for now. But they were already implimented, so they were left in app.  

About future TODOs:  
- add proper docks; 
- add tests;
- vrappers, that are located in data_management, should be done as classes, to ensure more broad and easier usage;  
- all endpoints that use @api_view - should be remake into classes for the same reason;  
As a side NOTE, functions were used as a starter, however time was closing too quickly, so they were left as a concept.
- impliment expiration time/date for teh tokens.

MAIN ENDPOINTS
- User authification:  
-- path("api/auth/", include("user_auth.urls")):  
--- Register user providing username, password and email:  
---- path("signup", view=views.signup);  
--- Login to system using username and password:  
---- path("login", view=views.login);  
--- Check if token working, returns user:  
---- path("check_token", view=views.check_token);  
--- GET all users or POST to create user:  
---- path("users", view=views.users);  
--- GET all info about certain user or PUT to edit certain user:  
---- path("users/<user_id>", view=views.users_by_id);  
- GET all restaurants or POST to create new restaurant:   
-- path("api/restaurants", restaurants_views.restaurants);  
- GET last menu for the particular restaurant or POST to create new menu for the restaurant:  
-- path("api/restaurants/<restaurant_id>/menu", restaurants_views.restaurants_by_id_last_menu);  
- GET menus for the current day:  
-- path("api/today_menus", menus_views.menus_current_day);  
- GET all votes or POST to create new vote:  
-- path("api/votes", votes_views.votes);  
- GET votes for each of the day`s menu:  
-- path("api/votes/calculate_today", votes_views.votes_calculate_for_today).