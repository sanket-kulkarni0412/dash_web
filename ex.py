from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table
from werkzeug.security import generate_password_hash
#sqlalchemy.sel select


db = SQLAlchemy()
engine = create_engine('sqlite:///static/login_cred.db')

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Unicode(128))
    username = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(1024))
    __tablename__ = 'login_table'
    __table_args__ = {'mysql_engine':'InnoDB'}

userTable = Table('login_table', User.metadata)
print("userTable =",userTable)
print("usermetadata=",User.metadata)

def create_user_table():
    User.metadata.create_all(engine)
create_user_table

# def add_user(email, password):
#     hashed_password = generate_password_hash(password, method='sha256')


#     conn = engine.connect()
#     select_stmt="select max(id) from control_panel_users"
#     results = conn.execute(select_stmt)
