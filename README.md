# Yandex backend-school test


## Development usage.
Use docker and docker-compose for development.

to run test use 
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
