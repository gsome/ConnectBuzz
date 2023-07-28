from flask import Flask, render_template, request, redirect, url_for
import os 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user,LoginManager, login_required,logout_user, current_user
from werkzeug.utils import secure_filename
import uuid as uuid


app = Flask(__name__)
direct = os.path.join("static", "pics")
app.config["UPLOAD_FOLDER"] = direct
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'my super secret key'

UPLOAD_FOLDER = 'static/pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader 
def load_user(user_id):
	return user.query.get(int(user_id))

# data base cionfiguration

class user(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200),nullable = False)
	country = db.Column(db.String(200),nullable = False)
	state = db.Column(db.String(200),nullable = False)
	location = db.Column(db.String(200),nullable = False)
	skill = db.Column(db.String(200),nullable = False)
	email = db.Column(db.String(200))
	number = db.Column(db.String(200),nullable = False, unique=True)
	image = db.Column(db.String(200),nullable = False)
	abt = db.Column(db.String(200),nullable = False)
	rating = db.Column(db.Integer)
	report = db.Column(db.Integer)
	password_hash = db.Column(db.String(200),nullable = False)
	date = db.Column(db.DateTime,default = datetime.utcnow)

	@property 
	def password(self):
		raise Attribute('password is not readable')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self, password_hash, password)
	
db.create_all()
#ALL pages and their route and endpoint
@app.route('/delete/<int:id>')
def delete(id):
	user_delete = user.query.get_or_404(id)

	try:
		db.session.delete(user_delete)
		db.session.commit()
		return redirect('/admin')
	except:
		return'opps'

@app.route("/")
def index():

	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	pic1 = os.path.join(app.config["UPLOAD_FOLDER"], "1.jpeg")
	pic2 = os.path.join(app.config["UPLOAD_FOLDER"], "2.webp")
	pic3 = os.path.join(app.config["UPLOAD_FOLDER"], "3.webp")
	return render_template("index.html", pic1=pic1, pic2=pic2, pic3=pic3, images=images)


@app.route("/home")
def home():


	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	pic1 = os.path.join(app.config["UPLOAD_FOLDER"], "1.jpeg")
	pic2 = os.path.join(app.config["UPLOAD_FOLDER"], "2.webp")
	pic3 = os.path.join(app.config["UPLOAD_FOLDER"], "3.webp")
	return render_template("index.html", pic1=pic1, pic2=pic2, pic3=pic3, images=images)

@app.route("/login")
def login():

	
	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	
	return render_template("login.html", images=images)

@app.route("/about")
def about():

	
	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	
	return render_template("about.html", images=images)



@app.route("/signup")
def signup():

	
	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	
	return render_template("signup.html", images=images)

@app.route("/adminlogin")
def adminlogin():
	
	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	
	return render_template("adminlogin.html", images=images)
	#return render_template("admin.html", images=images,search=search)


@app.route("/adminlo", methods=['POST'])
def adminlo():
	phone = request.form['phone']
	password = request.form['password']

	search = user.query
#	search = search.filter(user.skill.like('%' + jobname + '%'))
	search = search.order_by(user.name).all()
	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")

	if phone == 'i dont know the name ' :#and 
		if password == 'cyber_maphian':

			return render_template("admin.html", images=images,search =search)
		else:
			return'you are not a valid user'
	else:
		return'you are not a valid user'
	#return redirect('/admin')


# process and code for the search page for a login user
@app.route("/profilesearch", methods=['POST'])
def psearch():
	jobname = request.form['jobname']
	state = request.form['location']
	place = request.form['place']

	if jobname == "":
		return 'You did not specify a jobname'

	else:

		search = user.query
		search = search.filter(user.skill.like('%' + jobname + '%'))
		search = search.filter(user.state.like('%' + state + '%'))
		search = search.order_by(user.name).all()
		images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")

		return render_template("psearch.html",images=images, search=search,jobname=jobname)

#______________________________________________________________________________________
#form processing next

@app.route("/search", methods=['POST'])
def search():
	jobname = request.form['jobname']
	state = request.form['location']
	place = request.form['place']

	if jobname == "":
		return redirect('/home')

	else:


		search = user.query
		search = search.filter(user.skill.like('%' + jobname + '%'))
		search = search.filter(user.state.like('%' + state + '%'))
		search = search.order_by(user.name).all()

		images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
		return render_template('search.html', images=images, jobname=jobname, search=search)


@app.route("/verify", methods=['POST'])
def verify():
	phone = request.form['phone']
	password = request.form['password']

	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	
	message="Sorry this number does not exist"
	message2="wrong password try again"
	message1="You did not specify a Number"
	error4 = 'Sorry you left a field empty apart from email'
	#check number before login
	num = user.query.filter_by(number=phone).first()
	#password check
	password =check_password_hash(num.password_hash,password)
	
	#passs = user.query.filter_by(password_hash=passwords).first()

		
	try:
		if phone == "":
			return render_template("login.html", images=images, message1=message1)
		else:
			if num:
				if password:
					return render_template('user.html', images=images,num=num)
				else:
					return render_template('login.html', images=images,message2=message2)
			else:
				return render_template("login.html", images=images, message=message)

				#if passs:
				#if check_password_hash(user.password_hash.split,password):
				#phone == "1234" and password == "1234":
				#images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
					#login_user(num)
					#return render_template('user.html', images=images)
				#else:
	except:				#return render_template('login.html', images=images,message2=message2)
		return render_template("login.html", images=images, message=message)
	




@app.route("/process", methods=['POST'])
def process():
	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")

	name = request.form['usname']
	country = request.form['country']
	state = request.form['state']
	location = request.form['location']
	skill = request.form['sk']
	gmail = request.form['gmail']
	contact = request.form['contact']
	image = request.files['pf']
	abt = request.form['absk']
	password = request.form['password']
	repass = request.form['re-password']
	rating = 0
	report = 0

	#grab image name
	image_name = secure_filename(image.filename)
	
	
	# set image special name
	picname = str(uuid.uuid1()) + "_" + image_name
	#save image
	saver = request.files['pf']
	
	#change image to string
	image = picname
	success='Your signup was successful, please login below'
	error1 = 'your passwords are not the same'
	error2 = 'your password must be atleast 4 digit'
	error3 = 'Sorry this number belongs to another user'
	error4 = 'Sorry you left a field empty apart from email'
	error5 = 'Sorry you left a field empty apart from email'
	unique = user.query.filter_by(number=contact).first()

	if contact =="":
		return render_template('signup.html', error4=error4,images=images)
		
	else:
		if name == "":
			return render_template('signup.html', error5=error5,images=images)

		else:
			if len(password) >= 4:
				if password == repass:
					if unique == None:
						password = generate_password_hash(password)
						signup = user(name=name,country=country,state=state,location=location,skill=skill,email=gmail,number=contact,image=image,abt=abt,password_hash=password, report=report,rating=rating)
						db.session.add(signup)
						db.session.commit()
						saver.save(os.path.join(app.config['UPLOAD_FOLDER'], picname)) 
						return render_template('login.html', success=success, images=images)
					else:
						return render_template('signup.html', error3=error3,images=images)


				else:
					return render_template('signup.html', error1=error1,images=images)

			else:
				return render_template('signup.html', error2=error2,images=images)
			#return 'ok'
		#return render_template('signup.html', error4=error4,images=images)

@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit(id):
	update = user.query.get_or_404(id)


	message5 = 'Your Profile Was Updated Successfully, Please Login.'
	#country = request.form['country']
	#state = request.form['state']
	#location = request.form['location']
	#skill = request.form['sk']
	#gmail = request.form['gmail']
	#contact = request.form['contact']
	#newnumber = request.form['newnumber']
	#update.image = request.files['pf']
	#update.abt = request.form['absk']
	

	if request.method == "POST":
		images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
		update.name = request.form['usname']
		update.state = request.form['state']
		update.location = request.form['location']
		update.skill = request.form['sk']
		update.country = request.form['country']
		update.email = request.form['email']
		update.number = request.form['newnumber']
		update.abt = request.form['absk']
		try:
			db.session.commit()

			#return redirect('/login',message5=message5) 
			return render_template('login.html', images=images,message5=message5)



		except:
			return'sorry an error occured'
	else:
		return render_template('editprofile.html',update=update)

# technique for rating
@app.route("/rate/<int:id>", methods=['POST'])
def rate(id):
	rate = user.query.get_or_404(id)
	rate.rating


	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	

	if request.method == "POST":

		rate.rating += 1
		try:
			db.session.commit()

			#return redirect('/login',message5=message5) 
			return('Thanks For Rating')
		except:
			return'sorry an error occured'
	else:
		return ('invalid request')

@app.route("/report/<int:id>", methods=['POST'])
def report(id):
	report = user.query.get_or_404(id)
	report.report


	images = os.path.join(app.config["UPLOAD_FOLDER"], "images.jpg")
	

	if request.method == "POST":

		report.report += 1
		try:
			db.session.commit()

			#return redirect('/login',message5=message5) 
			return('Thanks For Reportng, If the issue involves froud please contact the admin directly at the top of this app or contact our Whatsap plateform')
		except:
			return'sorry an error occured'
	else:
		return ('invalid request')


app.run(host="0.0.0.0", port=5000) 