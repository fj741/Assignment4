from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt 
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, UserMixin
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psword123@localhost:5433/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

#I added a login manager to create a state where the user has logged in. This way it allows only users to create a blog

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return Info.query.get(int(id))

#The Info table stores all the information about the user including a hashed and salted password
class Info(db.Model, UserMixin):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hash = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Blog', backref="author",)
    
    
    
    def __init__(self, fname, lname, email, hash):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.hash = hash
#Created a Blog model so that users can create posts. I included a foreign key to connect the table to the Info table
class Blog(db.Model):
    __tablename__ = 'blog'
    blog_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(Info, backref=db.backref('blog', lazy=True))
    
    def __init__(self, title, content, user_id, user):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.user = user

#Checks connection to the database
@app.route('/check_connection')
def check_connection():
    try: 
        db.engine.connect().close()
        return "Connected to the database"
    except Exception as e:
        return "Couldn't connect to the databse"
    
#I created a custom 404 page if the user enters an ivalid url    
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')
            

@app.route('/')
def home():
    return render_template('home.html')

#If the request.method is POST, the information gets stored to a database
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return "Passwords do not match"
        
        
        
        '''To make sure that the email has not been taken I queried the database.'''
        existing_email = Info.query.filter_by(email=email).first()
        
        if existing_email():
            return redirect(url_for('register.html'))
        
        
        newUser = Info(fname=fname, lname=lname, email=email)
        newUser.hash = generate_password_hash(password)
        
        db.session.add(newUser)
        db.session.commit()
        return 'User was Created'
    else:
        return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = Info.query.filter_by(email=email).first()
    else:
        return render_template("login.html")
    
        

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        newBlog = Blog(title=title, content=content)
    else: 
        return render_template('create.html')    



#Run the app while debug=true. 
if __name__=='__main__':
    app.run(debug=True)