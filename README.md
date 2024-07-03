1. Build docker container:  
docker build .
2. Run docker container:
docker run container_id

TODO: fix docker having problems with building (because of psycorg2) and connecting to the DB  

1. Start postgres server;
1.5 Install all reuirements:
$ python3 -m pip install -r requirements.txt
2. Use comand to migrate all data:
$ python3 manage.py migrate

3. Create superuser:  
$ python3 manage.py createsuperuser  
4. Server should be avaible at 0.0.0.0:8000;
5. In test_endpoints.rest - there is manual starter of every endpoint avaible;
6. In every urls.py - brief explanation of what endpoint does;
7. All Models can be used in Admin. However, there are not configured fully