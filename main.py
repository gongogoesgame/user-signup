from flask import Flask, request, redirect, render_template


# functions required for validating signup_form input
def is_empty(str):
    if str == "":
        return True
    else:
        return False

def valid_username(username):
    if " " in username:
        return False
    if len(username) < 3 or len(username) > 20:
        return False
    return True

def valid_password(password):
    if " " in password:
        return False
    if len(password) < 3 or len(password) > 20:
        return False
    return True

def password_match(password, password_repeat):
    return password == password_repeat

def over_one_dot(str):
    str_list = str.split(".")
    if len(str_list) > 2:
        return True

def valid_email(email):
    if email != "":
        if " " in email:
            return False
        if len(email) < 3 or len(email) > 20:
            return False
        if "@" not in email:
            return False
        if over_one_dot(email):
            return False
    # no email is required thus empty string is a valid input
    return True


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def index():
    return redirect("/signup")

@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    title = "Welcome, " + username
    return render_template("welcome.html", 
                            username=username, 
                            title=title)

@app.route("/signup")
def display_signup():
    title = "Please sign up!"
    return render_template('signup_form.html', title=title,)

@app.route("/signup", methods=["POST"])
def validate_signup_form():
    username = request.form["username"]
    password = request.form["password"]
    password_repeat = request.form["password_repeat"]
    email = request.form["email"]
    
    # Validate input fields
    if is_empty(username):
        username_error = "User field cannot be left empty." 
    elif not valid_username(username):
        username_error = "This is not a valid username. Must be between 3 and 20 characters. No spaces allowed."
    else:
        username_error = ""

    if is_empty(password):
        password_error = "Password field cannot be left empty." 
    elif not valid_password(password):
        password_error = "Password must be 3 to 20 characters. No spaces allowed."
    else:
        password_error = ""

    if is_empty(password_repeat):
        password_repeat_error = "Password field cannot be left empty." 
    elif not password_match(password, password_repeat):
        password_repeat_error = "Passwords do not match"
    else:
        password_repeat_error = ""

    email_error = "" if valid_email(email) else "This is not a valid email. Must be 3 to 20 characters, one dot and no spaces."

    if (username_error=="" 
         and password_error=="" 
         and password_repeat_error=="" 
         and email_error==""):
        return redirect('welcome?username={}'.format(username))
    else:
        return render_template('signup_form.html', 
                username_error=username_error, 
                password_error=password_error, 
                password_repeat_error=password_repeat_error, 
                email_error=email_error,
                username=username,
                email=email)

if __name__ == "__main__":
    app.run()