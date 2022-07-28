import email
from os import name
from dash import callback
import dash
import dash_labs as dl
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import sqlite3

from annoy_ import *
import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, LoginManager, UserMixin
from ex import db, User as base


# app_flask = Flask(__name__)

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
def create_db():
    con = sqlite3.connect('static\\login_cred.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS login_table (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, 
    username TEXT TEXT NOT NULL UNIQUE ,
    password VARCHAR(25) NOT NULL UNIQUE)''')
    cur.execute('SELECT * FROM login_table')
    con.commit()

    result = cur.fetchall()
    con.close()

    # print('db_created', result)


create_db()

app_flask = Flask(__name__)

external_stylesheets = [dbc.themes.GRID, dbc.themes.BOOTSTRAP]

app = Dash(server=app_flask, external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True)

app_flask.config.update(SECRET_KEY='thisissecret',
                        SQLALCHEMY_DATABASE_URI='sqlite:///static/login_cred.db',
                        SQLALCHEMY_TRACK_MODIFICATIONS=True)

db = SQLAlchemy(app_flask)

db.init_app(app_flask)

login_manager = LoginManager()
login_manager.init_app(app_flask)
login_manager.login_view = '/login'

# class flask_login.UserMixin
# This provides default implementations for the methods that Flask-Login expects user objects to have.


class User(UserMixin, base):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    # return User.query.filter_by(username=user_id).first()

#==========================NAVBAR AT LOGIN PAGE=================================#


navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Create Profile", href="/create_profile"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="/home",
    color="primary",
    dark=True,
)
#==========================NAVBAR AT ANNOY PAGE=================================#

navbar_logout = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("LOGOUT", href="/logout"),
                dbc.DropdownMenuItem("UPDATE", href="/update_page")
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="/home",
    color="primary",
    dark=True,
)

#==========================APP_LAYOUT=================================#


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

home_page = html.Div(children=[
    html.H1(children='Image recommendation',
            style={'textAlign': 'center'}),
    html.Div(children='''
        Upload Image from any of them will give the
         recommendations of 6 images from dataset.
    ''', style={'textAlign': 'center'}),
    dbc.Button("Click here to Login", id="example-button", href="/login",
               external_link=True, color="primary", type='Button', style={'margin-top': '100px', 'textAlign': 'center',
                                                                          'margin-left': '45%'}),
])

#==========================LOGIN PAGE=================================#


Login_page = html.Div(children=[
    (navbar),
    html.H1('Annoy Search', style={'textAlign': 'center'}),
    html.H2('Login', style={'textAlign': 'center'}),
    dcc.Input(id="username", type="email", placeholder="Enter Your Email", className="inputbox1", style={'margin-left': '35%', 'width': '450px',  'textAlign': 'center','height': '45px', 'padding': '10px', 'margin-top': '60px',
                                                                                                         'font-size': '16px', 'border-width': '3px', 'border-color': '#a0a3a2'
                                                                                                         }),
    dcc.Input(id="passwrd", type="password", placeholder="Enter Password", className="inputbox2", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center', 'height': '45px', 'padding': '10px', 'margin-top': '60px',
                                                                                                         'font-size': '16px', 'border-width': '3px', 'border-color': '#a0a3a2'
                                                                                                         }),
    dbc.Button(
        "Sign In", id="button", className="me-2", n_clicks=0, style={'margin-top': '100px', 'textAlign': 'center',
                                                                     'margin-left': '45%'}),
    html.Div(id='output_comment')
])


@callback(Output('output_comment', 'children'),
          [Input('button', 'n_clicks')],
          [State('username', 'value')],
          [State('passwrd', 'value')],
          )
def login_access(clicks, user_, password):
    if user_ != password:

        con = sqlite3.connect('static/login_cred.db')
        cur = con.cursor()
        cur.execute(
            'SELECT * FROM login_table WHERE username = ? AND password = ?', (user_, password))
        result = cur.fetchall()

        user = User.query.filter_by(username=user_).first()

        # print(password)
        login_user(user)
        if len(result) == 1:
            # print(current_user.is_authenticated)
            return html.Div(dcc.Link('Click here to Upload Image', href='/upload_image',
                                     style={'color': 'green', 'font-family': 'serif', 'font-weight': 'bold',
                                            "text-decoration": "none", 'font-size': '20px'}),
                            style={'padding-left': '605px', 'padding-top': '40px'})
        else:

            return html.Div(html.A('Incorrect Username or Password', href='/home_page',
                                   style={'color': 'red', 'font-family': 'serif', 'font-weight': 'bold',
                                          "text-decoration": "none", 'font-size': '20px'}),
                            style={'padding-left': '605px', 'padding-top': '40px'})  # href='/create_profile',

#==========================CREATE ID=================================#


Create_page = html.Div(children=[
    html.H1('Annoy Search', style={'textAlign': 'center'}),
    html.H2('Create Profile', style={'textAlign': 'center'}),

    dcc.Input(id="create_name", type="text", placeholder="Name", className="inputbox1", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center',
                                                                                               'height': '45px', 'padding': '10px', 'font-size': '16px',
                                                                                               'border-width': '3px', 'border-color': '#a0a3a2'}),

    dcc.Input(id="create_username", type="email", placeholder="Email", className="inputbox2", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center',
                                                                                                     'height': '45px', 'padding': '10px', 'font-size': '16px',
                                                                                                     'border-width': '3px', 'border-color': '#a0a3a2'}),

    dcc.Input(id="create_passwrd", type="password", placeholder="Password", className="inputbox3", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center',
                                                                                                          'height': '45px', 'padding': '10px', 'font-size': '16px',
                                                                                                          'border-width': '3px', 'border-color': '#a0a3a2'}),

    dcc.Input(id="confirm_passwrd", type="password", placeholder="Confirm Password", className="inputbox4", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center',
                                                                                                                   'height': '45px', 'padding': '10px', 'font-size': '16px',
                                                                                                                   'border-width': '3px', 'border-color': '#a0a3a2'}),
    dbc.Button("Create", id="submit_button",  n_clicks=0,style={'margin-top': '100px','textAlign': 'center','margin-left': '45%'}),

    html.Div(id='created_comment')])


@callback(Output('created_comment', 'children'),
          [Input('submit_button', 'n_clicks')],
          [State('create_name', 'value')],
          [State('create_username', 'value')],
          [State('create_passwrd', 'value')],
          [State('confirm_passwrd', 'value')])
def login_access(clicks, name, username, password, con_password):
    if password == con_password:
        con = sqlite3.connect('static/login_cred.db')
        # cur=con.cursor()
        con.executemany('INSERT INTO login_table (name,username,password) VALUES (?,?,?);', [
                        (name, username, con_password)])
        con.commit()
        cur = con.cursor()
        result = cur.fetchall()
        con.close()
        print('dbs:', result)
        return html.Div(dcc.Link('Submit and Click here to Login', href='/login',
                                 style={'color': '#183d22', 'font-family': 'serif', 'font-weight': 'bold',
                                        "text-decoration": "none", 'font-size': '20px'}),
                        style={'padding-left': '605px', 'padding-top': '40px'})
    else:
        return html.Div(html.H3('Please fill the details properly',
                                style={'color': '#183d22', 'font-family': 'serif', 'font-weight': 'bold',
                                       "text-decoration": "none", 'font-size': '20px'}),
                        style={'padding-left': '605px', 'padding-top': '40px'})


#==========================UPDATE=================================#
update_page = html.Div(children=[
    html.H1('Annoy Search', style={'textAlign': 'center'}),
    html.H2('Update Profile', style={'textAlign': 'center'}),
    dcc.Input(id="update_name", type="text", placeholder="Name", className="inputbox1", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center',
                                                                                               'height': '45px', 'padding': '10px', 'font-size': '16px',
                                                                                               'border-width': '3px', 'border-color': '#a0a3a2'}),
    dcc.Input(id="new_password", type="password", placeholder="New Password", className="inputbox1", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center',
                                                                                                            'height': '45px', 'padding': '10px', 'font-size': '16px',
                                                                                                            'border-width': '3px', 'border-color': '#a0a3a2'}),
    dcc.Input(id="confirm_new_password", type="password", placeholder="Confirm New Password", className="inputbox1", style={'margin-left': '35%', 'width': '450px', 'textAlign': 'center',
                                                                                                                            'height': '45px', 'padding': '10px', 'font-size': '16px',
                                                                                                                            'border-width': '3px', 'border-color': '#a0a3a2'}),
    dbc.Button(
        "Update", id="update_button",  n_clicks=0,style={'margin-top': '100px', 'textAlign': 'center',
                                                                          'margin-left': '45%'}),
    html.Div(id='updated_comment')
])


@callback(Output('updated_comment', 'children'),
          [Input('update_button', 'n_clicks')],
          [State('update_name', 'value')],
          [State('new_password', 'value')],
          [State('confirm_new_password', 'value')]
          )
def login_access(clicks, name, up_pass, con_newpass):
    if con_newpass:
        if up_pass == con_newpass:
            con = sqlite3.connect('static/login_cred.db')
            cur = con.cursor()
            email = current_user.username
            print(email)
            cur.execute('UPDATE login_table SET name=?,password=? WHERE username=?',
                        (name, con_newpass, email))
            con.commit()
            print('done')
            result = cur.fetchall()
            con.close()
            print('dbs:', result)
            return html.Div(dcc.Link('Submit and Click here to Login', href='/login',
                                     style={'color': '#183d22', 'font-family': 'serif', 'font-weight': 'bold',
                                            "text-decoration": "none", 'font-size': '20px'}),
                            style={'padding-left': '605px', 'padding-top': '40px'})
        else:
            return html.Div(html.H3('Incorrect Data',
                                    style={'color': '#183d22', 'font-family': 'serif', 'font-weight': 'bold',
                                           "text-decoration": "none", 'font-size': '20px'}),
                            style={'padding-left': '605px', 'padding-top': '40px'})


#==========================ANNOY IMAGE SEARCH=================================#
image_search_page = html.Div(children=[
    (navbar_logout),
    html.H1('Annoy Search Image', style={'textAlign': 'center'}),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-image-upload')
])


def bs64_image(img):
    with open(img, 'rb') as ima:
        data = base64.b64encode(ima.read())
        data = data.decode('utf-8')
        contents = "data:image/jpeg;base64," + data
        # image_output.append(img)
    return contents


@callback(Output('output-image-upload', 'children'),
          [Input('upload-image', 'contents')], [State('upload-image', 'filename')])
def get_images(list_of_contents, name_list):
    if name_list:
        # print(list_of_contents)
        # # print(list_of_contents[0])
        file_content = list_of_contents.replace("data:image/jpeg;base64,", "")
        # print("file_content :", file_content)
        imgdata = base64.b64decode(file_content)
        # print(imgdata)
        filename = 'test.jpg'
        with open(filename, 'wb') as f:
            f.write(imgdata)
        image_list = out_put_of_images(filename)
        img1 = bs64_image(image_list[0])
        img2 = bs64_image(image_list[1])
        img3 = bs64_image(image_list[2])
        img4 = bs64_image(image_list[3])
        img5 = bs64_image(image_list[4])
        img6 = bs64_image(image_list[5])
        row_list = [dbc.Row([
                    dbc.Col(html.Img(src=img1, width=400)),
                    dbc.Col(html.Img(src=img2, width=400)),
                    dbc.Col(html.Img(src=img3, width=400))
                    ]),
                    dbc.Row([
                        dbc.Col(html.Img(src=img4, width=400)),
                        dbc.Col(html.Img(src=img5, width=400)),
                        dbc.Col(html.Img(src=img6, width=400))
                    ])]
        return row_list
    return html.Div()

#==========================APP CALLBACK=================================#


@ app.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/upload_image':
        if current_user.is_authenticated:
            return image_search_page
        else:
            return Login_page
    elif pathname == '/logout':
        logout_user()
        return home_page
    elif pathname == '/update_page':
        return update_page
    elif pathname == '/home':
        logout_user()
        return home_page
    elif pathname == '/login':
        return Login_page
    elif pathname == '/create_profile':
        return Create_page
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
