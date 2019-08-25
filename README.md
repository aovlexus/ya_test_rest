# Yandex backend-school entering test

## Description

### Technology stack:
- Django
- Django rest framework
- PostgreSQL 

### Project structure:
```
+ conf # configuration and requirements 
+ deploy # ansible cofiguration that allow deliver data to server 
+ docker # helping files to make docker infrastructure 
+ ya_test # django project root
```

### Django project contains two apps:
 - core: usual using for define some core features as Abstract models etc... Din't use for now
 - imports: app with all imports-related functionality
 
### Test
For testing in this project pytest is used. All tests are located in *_tests.py files.
E.g. tests for `views.py` are in `views_tests.py`. See Development usage to 
run tests. 

## Development usage.
Use docker and docker-compose for development.

To run tests use 
```bash
local-user$ docker-compose run ya_test sh
/usr/src/app/ya_test# pytest
```


## Production usage
### Deploy to current server:
To deploy new verision to server run
```bash
ansible-playbook  -i ./deploy/hosts --ask-become-pass  ./deploy/deploy.yml
```
and enter sudo password. It requires to restart supervisor and nginx.

### deploy to new servers:
service system requirements
 - postgresql:10
 - python3.6
 - nginx

superviser and other software will be installed automatically
