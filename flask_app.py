
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, make_response, request, render_template
import io
import csv
import pandas as pd
from processing import compare_csv

app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return render_template("main_page.html")

#@app.route("/login/", methods=["GET", "POST"])
#def login():
#    return render_template("login_page.html")

@app.route('/transform', methods=["GET","POST"])
def transform_view():

    roll_no = request.form["roll_no"]
    print(roll_no)

    f = request.files['data_file']

    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = list(csv.reader(stream))
    #print("file contents: ", file_contents)
    #print(type(file_contents))
    with open('mysite/test.csv','r') as f:
        correct_csv = list(csv.reader(f))

    print(correct_csv)

   #  file2_line = rdr2.next()


    #print(csv_input)

    accuracy = compare_csv(csv_input, correct_csv)

    with open('results_raw.csv','a') as fd:
        print("Writing :" + roll_no+"," + str(accuracy) + "\n")
        fd.write(roll_no+"," + str(accuracy)+ "\r")



    #stream.seek(0)
    #result = transform(stream.read())

    #response = make_response(result)
    #response.headers["Content-Disposition"] = "attachment; filename=result.csv"

    return render_template('accuracy_page.html', accuracy = accuracy)
    #return """
    #    <html>
    #        <body>
    #            <h3>Current Submission Accuracy is</h3> {accuracy}
    #        </body>
    #    </html>
    #""".format(accuracy = accuracy)

@app.route('/lb')
def html_table():
    df = pd.read_csv('results_raw.csv')
    df = df.sort_values(df.columns[1], ascending=False).drop_duplicates([df.columns[0]])

    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


