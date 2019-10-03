
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, make_response, request, render_template
import io
import csv
#import pandas as pd

app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return render_template("main_page.html")

@app.route('/transform', methods=["GET","POST"])
def transform_view():

    roll_no = request.form["roll_no"]
    print(roll_no)

    f = request.files['data_file']

    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    #print("file contents: ", file_contents)
    #print(type(file_contents))

    correct_csv = csv.reader("test.csv")


    print(csv_input)

    error_count = 0
    total_count = 0

    for line in csv_input:
        total_count = total_count + 1
        if line not in correct_csv:
            error_count = error_count + 1

    accuracy = error_count / total_count * 100

    with open('results_raw.csv','a') as fd:
        print("Writing :" + roll_no+"," + str(accuracy))
        fd.write(roll_no+"," + str(accuracy))



    #stream.seek(0)
    #result = transform(stream.read())

    #response = make_response(result)
    #response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return """
        <html>
            <body>
                <h1>Accuracy is</h1> {accuracy}
            </body>
        </html>
    """.format(accuracy = accuracy)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


