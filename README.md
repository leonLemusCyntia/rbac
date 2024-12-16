# RBAC
Diagrams and Documentation
https://miro.com/app/board/uXjVL2lQZjU=/

# Run project
1. Build containers
```
docker compose up -d --build
```
2. Create modules in DB
```
$docker exec -ti arkham-rbac-1 /bin/bash
app# flask shell
>>> db.create_all()
```
3. Insert values using Adminer as shown in diagram
4. Execute calls to payments service using different users

# Run tests
Run tests from docker containers if packages are not installed in your dev environment,
otherwise run the test from each project paths
```
pytest test_app.py
```
