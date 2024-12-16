from flask import Flask, abort, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from json import dumps


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:admin@db:5432/rbac"
port = 3000
db.init_app(app)


Role_Permission_Relationship = Table(
    "role_permission_relationship",

    Base.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role")


@app.route("/")
def home():
    return "Hello, this is a RBAC Flask Microservice"

@app.route("/rbac-auth", methods=["GET"])
def get_rbac_auth():
    user_id = int(request.args["user_id"])
    permission = request.args["permission"]
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    permission = db.session.query(Permission).filter(Permission.name == permission).first_or_404()
    grant_permission = db.session.query(
        Role_Permission_Relationship
    ).filter(
        Role_Permission_Relationship.c.role_id == user.role.id,
        Role_Permission_Relationship.c.permission_id == permission.id
    ).first()
    if grant_permission is None:
        abort(403)
    return jsonify({"message": "ok"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=port)




