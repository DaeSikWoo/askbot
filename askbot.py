from flask import Flask, render_template, request, redirect, url_for
import logging
import mysql.connector

app = Flask(__name__)

# Configure logging settings
logging.basicConfig(filename='/your/log/path/logfile.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Add logger
logger = logging.getLogger('request_logger')

# Establish connection to MySQL
mysql_connection = mysql.connector.connect(
    host='your localhost',
    user='your user',
    password='your password',
    database='your database'
)
mysql_cursor = mysql_connection.cursor()

# Retrieve data from MySQL
mysql_cursor.execute('SELECT rule, response FROM your table')
chatbot_data = mysql_cursor.fetchall()

# chat_dic 초기화
chat_dic = {}
for row in chatbot_data:
    rule = row[0]
    response = row[1]
    chat_dic[rule] = response

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        req = request.form['user_input']
        if req == 'exit':
            return render_template('index.html', response='프로그램을 종료합니다.')
        else:
            response = chat(req)
            logger.info(f"Request: {req}")  # Log the request
            return render_template('index.html', response=response)

    else:
        return render_template('index.html')


def chat(request):
    for rule, response in chat_dic.items():
        index = -1
        for word in rule.split('|'):
            try:
                if index == -1:
                    index = request.index(word)
                else:
                    if index < request.index(word, index):
                        index = request.index(word, index)
                    else:
                        index = -1
                        break
            except ValueError:
                index = -1
                break

        if index > -1:
            return response

    return '이해하지 못했습니다. 다시 한 번 말씀해주시겠어요?'

# adding data
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        # Process the form data and add it to the database
        req = request.form['request']
        rule = request.form['rule']
        response = request.form['response']

        # Insert the data into the database
        insert_query = "INSERT INTO your table (request, rule, response) VALUES (%s, %s, %s)"
        insert_values = (req, rule, response)
        mysql_cursor.execute(insert_query, insert_values)
        mysql_connection.commit()

        return redirect(url_for('add_data'))  # Redirect to the same page after adding data

    # Fetch the stored data from the database
    select_query = "SELECT id, request, rule, response FROM your table"
    mysql_cursor.execute(select_query)
    stored_data = mysql_cursor.fetchall()

    return render_template('add_data.html', stored_data=stored_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0' port='5000')
