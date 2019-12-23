
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, make_response, request, render_template
import io
import csv
import pandas as pd
from processing import compare_csv

app = Flask(__name__)


@app.route('/cacheon')
def landing():
    return render_template("landing.html")

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
    with open('mysite/correct_ans.csv','r') as f:
        correct_csv = list(csv.reader(f))

    print(correct_csv)

   #  file2_line = rdr2.next()


    #print(csv_input)

    accuracy = compare_csv(csv_input, correct_csv)

    with open('results_raw.csv','a') as fd:
        print("Writing :" + roll_no+"," + str(accuracy) + "\n")
        fd.write(roll_no+"," + str(accuracy)+ "\r")



    # Plotting submission history
    df = pd.read_csv('results_raw.csv')
    df_roll = df.loc[df['Roll Number'] == roll_no]
    acc_list = df_roll[' Accuracy'].values.tolist()
    sub_no_list = range(1,len(acc_list)+1)
    print(sub_no_list)

    #stream.seek(0)
    #result = transform(stream.read())

    #response = make_response(result)
    #response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    if accuracy <20:
        message = "Ouch!! Worse than random guessing! Something went horribly wrong."
    if accuracy >=20 and accuracy <39:
        message = "Hey, better than Random guessing! If training accuracy was much better, you are overfitting."
    if accuracy >=39 and accuracy <50:
        message = "Just passing! If training accuracy was much better, you are overfitting."
    if accuracy >=50 and accuracy <70:
        message = "Some learning is happening. Try tuning the parameters better."
    if accuracy >=70 and accuracy <80:
        message = "Almost beating some really good people from best universities!"
    if accuracy >=80 and accuracy <85:
        message = "Congrats! Tune some more and soon you will be contributing to science!"
    if accuracy >=85:
        message = "Time to write that paper!!"
    if accuracy >=85 and roll_no=='Apna Time Aayega':
        message = "Apna time aayega? More like apna time AA GAYA!!"
    if accuracy >=85 and roll_no=='SCAM':
        message = "Whadda Scam!! Lets Scam science now!"
    if accuracy >=85 and roll_no=='515':
        message = "Aila GILLA!!"
    if accuracy >=85 and roll_no=='Apna time aa raha hai':
        message = "Kaun Bola - 'Mujhse na ho payega!'? KAUN BOLA?"
    if accuracy >=85 and roll_no=='':
        message = "Shine on you Nameless Diamond!"

    return render_template('accuracy_page.html', accuracy = accuracy, message = message, labels = sub_no_list, values = acc_list,title='Your Submission History', max=100)

@app.route('/lb')
def html_table():
    df = pd.read_csv('results_raw.csv')
    df = df.sort_values(df.columns[1], ascending=False).drop_duplicates([df.columns[0]])
    df = df.reset_index()
    del df['index']
    return render_template('simple.html',  tables=[df.to_html(classes='data',
                       bold_rows = True, border =2,
                       col_space = 100,
                       justify = 'center',
                       na_rep =' ')], titles=df.columns.values)

@app.route('/chart')
def plot_history():
    a = [1,2,3,4]
    lab = ['a','b','c','d']
    return render_template('bar_chart.html',title='Bitcoin Monthly Price in USD', max=5, values = a, labels = lab)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


