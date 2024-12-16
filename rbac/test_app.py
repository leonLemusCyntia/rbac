from pathlib import Path
import pytest

from .app import app, db, Role, Permission, Role_Permission_Relationship, User

TEST_DB = "test.db"

@pytest.yield_fixture(scope='function')
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    app.config["DATABASE"] = BASE_DIR.joinpath(TEST_DB)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR.joinpath(TEST_DB)}"

    with app.app_context():
        db.create_all()  # setup
        yield app.test_client()  # tests run here
        db.session.close()
        db.drop_all()  # teardown

def test_home(client):
    response = client.get("/", content_type="html/text")
    assert response.status_code == 200

def test_rbac_auth(client):
    role_admin = Role(name="Admin")
    role_user = Role(name="User")

    db.session.add(role_admin)
    db.session.add(role_user)
    db.session.commit()

    permission_read = Permission(name="READ_PAYMENTS")
    permission_insert = Permission(name="INSERT_PAYMENTS")

    db.session.add(permission_read)
    db.session.add(permission_insert)
    db.session.commit()

    admin_user = User(username="User admin", role_id=role_admin.id)
    reg_user = User(username="User reg", role_id=role_user.id)

    db.session.add(admin_user)
    db.session.add(reg_user)
    db.session.commit()

    r_1 = Role_Permission_Relationship.insert().values(role_id=role_admin.id, permission_id=permission_read.id)
    db.session.execute(r_1)
    r_2 = Role_Permission_Relationship.insert().values(role_id=role_admin.id, permission_id=permission_insert.id)
    db.session.execute(r_2)
    r_3 = Role_Permission_Relationship.insert().values(role_id=role_user.id, permission_id=permission_read.id)
    db.session.execute(r_3)
    db.session.commit()

    # test non-existing user and permission
    response = client.get("/rbac-auth", query_string={"user_id": 3322, "permission": permission_read.name})
    assert response.status_code == 404

    response = client.get("/rbac-auth", query_string={"user_id": admin_user.id, "permission": 'non-existing-permission'})
    assert response.status_code == 404

    # Testing permissions for admin
    response = client.get("/rbac-auth", query_string={"user_id": admin_user.id, "permission": permission_read.name})
    assert response.status_code == 200

    response = client.get("/rbac-auth", query_string={"user_id": admin_user.id, "permission": permission_insert.name})
    assert response.status_code == 200

    # Testing permissions for reg user
    response = client.get("/rbac-auth", query_string={"user_id": admin_user.id, "permission": permission_read.name})
    assert response.status_code == 200

    response = client.get("/rbac-auth", query_string={"user_id": reg_user.id, "permission": permission_insert.name})
    assert response.status_code == 403






    
    
    