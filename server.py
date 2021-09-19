from flask import Flask, render_template, request, redirect, url_for
import os
import glob
import sqlite3 as sql
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path = "/upload", static_folder = "upload")

app.config['SECRET_KEY'] = 'itsasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['CSRF_ENABLED'] = True 
app.config['USER_ENABLE_EMAIL'] = False 

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_cursor_and_db_conn():
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    return (cursor, conn)

def get_listing_rows():
    (cursor, _) = get_cursor_and_db_conn()
    cursor.execute("SELECT rowid, * FROM listings")
    return cursor.fetchall()

def initialize_db():
    (cursor, conn) = get_cursor_and_db_conn()

    # Check if table exists already
    listings_exist = False
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='listings' ''')

    #if the count is 1, then the table exists
    if cursor.fetchone()[0]==1 : 
        print('Listings table exists.')
        listings_exist = True
    
    if listings_exist:
        num_rows = len(get_listing_rows())
        if num_rows > 0:
            print("listings table has entries")
        print("Retrieved %d database entries" % num_rows)
    else:
        print("Creating listings table")
        # Create listings table with sample data
        cursor.execute("DROP TABLE IF EXISTS listings")
        cursor.execute("CREATE TABLE listings (name TEXT, desc TEXT, \
            c_info TEXT, price REAL, \
            imgPath TEXT, isPrivate BOOL, \
            user TEXT)")
    
    conn.commit()
        
    # Setup User DB if needed
    db_exists = os.path.isfile("./database.db")
    if not listings_exist:
        db.create_all()
        db.session.commit()
        print("Created User db!")
        
    print("Initialized database")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loggingIn", methods = ['GET', 'POST'])
def loggingIn():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        if name == "" or password == "":
            return render_template("login.html", message="Please fill out both fields")

        user = User.query.filter_by(username=name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)

    return redirect(url_for("home_page"))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':

        # Check if the form's empty
        name = request.form['username']
        password = request.form['password']
        if name == "" or password == "":
            return render_template("signup.html", message="Please fill out both fields")

        # Check if the user already exists
        user = User.query.filter_by(username=name).first()
        if user:
            return render_template("signup.html", message="User already exists. Please choose a different name.")

        # Hash the password and store it
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print("New User has been created!")

    return redirect(url_for("home_page"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/")
@login_required
def home_page():
    (cursor, _) = get_cursor_and_db_conn()

    # Get all db info for the images so it can be displayed
    rows = get_listing_rows()
    listings = []
    for row in rows:
        # If a listing is private and we aren't the user that posted it
        # we skip it
        if ((str(row[6]) == "1") and (row[7] != current_user.username)):
            continue

        # Append info to listings that we show to the user
        listings.append({
            "id":                       row[0],
            "name":                     row[1],
            "desc":                     row[2],
            "c_info":                   row[3],
            "price": "$%.2f" %          row[4],
            "imgSrc": "/upload/%s" %    row[5]
        })

    return render_template("index.html", listings=listings, username=current_user.username)

@app.route("/remove/<listing_id>")
def remove(listing_id):
    if not listing_id:
        return render_template("imgUpload.html", message="listing ID does not exist!")

    (cursor, conn) = get_cursor_and_db_conn()

    # Get the path for the image
    cursor.execute("SELECT imgPath FROM listings WHERE rowid = ?", (listing_id,))
    imgPath = str(cursor.fetchone()[0])

    # Delete the image itself
    filename = "./upload/"+imgPath
    f = glob.glob(filename)[0]
    os.remove(f)

    # Delete the db entry for the image
    cursor.execute("DELETE FROM listings WHERE rowid = ?", (listing_id,))
    conn.commit()
    print("Image Removed!")
    return redirect(url_for("home_page"))
    
@app.route("/addImg")
def addImg():
    # initialize_db()
    return render_template("imgUpload.html", message="Enter your image's characteristics below!")

@app.route("/clearUserImages")
@login_required
def clearUserImages():
    (cursor, conn) = get_cursor_and_db_conn()

    # Get paths all of user's images regardless of if they're private or not
    cursor.execute("SELECT imgPath FROM listings WHERE user = ?", (current_user.username,))
    paths = cursor.fetchall()
    img_paths = []
    for path in paths:
        img_paths.append(path[0])
    
    cursor.execute("DELETE FROM listings WHERE user = ?", (current_user.username,))  
    # Commit the db changes
    conn.commit()
    
    for path in img_paths:
        filename = "./upload/"+path
        f = glob.glob(filename)[0]
        os.remove(f)

    print("Cleared user images!")

    return render_template("dbClearSuccess.html")

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if request.method == 'POST':

        # Check what's missing from the form
        missing_contents = []
        name = request.form['image_name']
        if name == "":
            missing_contents.append("name")
        description = request.form['desc']
        contact_info = request.form['c_info']
        if contact_info == "":
            missing_contents.append("contact info")
        price = request.form['price']
        if not price:
            # can't store empty price in db
            missing_contents.append("price")
        f = request.files['file']
        if not f:
            missing_contents.append("image")
        is_private = request.form['is_private']

        # If we have missing information for a listing we prompt the user to fill in the form
        num_missing = len(missing_contents)
        if num_missing > 0:
            msg = "Please enter a value for "
            if num_missing == 1:
                msg = msg + "the "+missing_contents[0]+"."
            else:
                for i in range(num_missing):
                    if i == (num_missing - 1):
                        msg = msg + "and the "+ missing_contents[i]+"."
                    else:
                        msg = msg + "the "+ missing_contents[i] + ", "
            return render_template("imgUpload.html", message=msg)

        (cursor, conn) = get_cursor_and_db_conn()

        # Check if there's an image with the same filename already in the db
        stored_path = "images/" + str(f.filename)
        cursor.execute("SELECT imgPath FROM listings WHERE imgPath = ?", (stored_path,))
        result = cursor.fetchone()
        if result is not None:
            msg = "Image repo already contains "+f.filename
            return render_template("imgUpload.html", message=msg)

        # Save the image if all checks pass
        relative_path = os.path.join("./upload/images", f.filename)
        f.save(relative_path)


        if not current_user.is_authenticated:
            used_name = "test"
        else:
            used_name = current_user.username

        cursor.execute("""INSERT INTO listings (name, desc, c_info, price, imgPath, isPrivate, user) VALUES \
        ('"""+name+"""', '"""+description+"""', '"""+contact_info+"""', """+price+""", \
        'images/"""+ f.filename +"""', """+is_private+""", '"""+used_name+"""')
        """)

        # Commit the db changes
        conn.commit()
        return redirect(url_for("home_page"))

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
