from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/selector', methods=['POST', 'GET'])
def selector():
    if request.method == 'POST':
        username = request.form.get('username')
        # Pass username to the next page
        return render_template('selector.html', username=username)
    return render_template('selector.html')

@app.route('/suggestions', methods=['POST'])
def suggestions():
    # Get data from form
    vibe = request.form.get('mood')
    name = request.form.get('username', '')  # optional — passed from login or selector

    # Render suggestions page with the correct variables
    return render_template('suggestions.html', name=name, vibe=vibe)

if __name__ == '__main__':
    app.run(debug=True)
