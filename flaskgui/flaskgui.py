from flask import Flask, render_template, request, url_for, request
app = Flask(__name__)

# Route for handling the login page logic
@app.route('/gui', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        result = request.form
    return render_template('gui.html', error=error)

if __name__ == '__main__':
   app.run(debug = True)
