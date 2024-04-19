from flask import Flask, render_template, request
from utils import locate_con_sequences_and_add_refs, find_tf_ids

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tfbs_locator', methods=['GET', 'POST'])
def tfbs_locator():
    if request.method == 'POST':
        input_string = request.form['input_string']
        data = locate_con_sequences_and_add_refs(input_string)
        return render_template('tfbs_locator.html', data=data)
    return render_template('tfbs_locator.html')

@app.route('/tf_finder', methods=['GET', 'POST'])
def tf_finder():
    if request.method == 'POST':
        input_string = request.form['input_string']
        data = find_tf_ids(input_string)
        return render_template('tf_finder.html', data=data)
    return render_template('tf_finder.html')

@app.route('/about_us')
def about_us():
    images = [
        "static/varun.jpg"
    ]
    return render_template('about_us.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
