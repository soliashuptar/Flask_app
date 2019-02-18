from flask import Flask, render_template, request, url_for, redirect
from twitter2 import create_map, get_data, get_location
app = Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/map")
def create_app():
    """
    Function renders a page with a map
    """
    return render_template("Map1.html")


@app.route("/", methods=['GET', "POST"])
def login():
    """
    Function renders a page with login form and directs to function which renders a map
    """
    try:
        if request.method == "POST":
            user_n = request.form['username']
            create_map(get_location(get_data(user_n)))
            return redirect(url_for("create_app"))
        return render_template('page.html')
    except:
        return render_template('page.html')


if __name__ == "__main__":
    app.run(debug=True)
