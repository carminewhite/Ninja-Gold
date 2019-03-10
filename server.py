from random import randint
from flask import Flask, render_template, redirect, session, request
from datetime import datetime


# print("date and time:",date_time)	



app = Flask(__name__)
app.secret_key = 'super secret'
@app.route('/')
def hello_world():
    #check and see if this is the initial loading screen
    if 'gold_processed' in session:
        pass
    else:
        session['user_gold'] = 0
        session['gold_processed'] = 0  #so destroy session doesn't break it
        session['property_processed'] = ""

    if 'submitted' in session:
        pass
    else:
        session['submitted'] = []
    #counter
    session['attempts'] += 1
    attempts = session['attempts']
    print ("////////", session['attempts'], "////////")
    your_gold = session['user_gold']
    activities = session['submitted']
    # print(session['submitted'][1]['timestamp'])


    return render_template('index.html', your_gold = your_gold, activity = activities, attempt = attempts)

@app.route('/process_gold', methods=['POST'])
def process_gold():
    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y %I:%M:%S %p")

    print("*"*50,"\nGold type clicked:", request.form['gold_name'])
    gold_dict = {
        "farm": randint(10,20),
        "cave": randint(5,10),
        "house": randint(2,5),
        "casino": randint(0,50)
    }
    #random chance whether casino is negative or positive
    if randint(0,500) > 250:
        random_casino = gold_dict['casino'] #return positive of casino
    else:
        random_casino = gold_dict['casino'] - gold_dict['casino'] - gold_dict['casino'] #return negative of casino
    gold_dict['casino'] = random_casino #assign positive or negative to the dictionary
    
    print("Amount to return: ", gold_dict[request.form['gold_name']])
    session['gold_processed'] = gold_dict[request.form['gold_name']]
    session['property_processed'] = request.form['gold_name']
    session['user_gold'] = session['user_gold'] + session['gold_processed']
    
    print("session gold_processed:", session['gold_processed'])


    if session['submitted'] == {} :
        session['submitted'] = {
            "gold" : session['gold_processed'],
            "property" : session['property_processed'],
            "timestamp" : date_time,
        }
    else:
        session['submitted'].insert(0,({
            "gold" : session['gold_processed'],
            "property" : session['property_processed'],
            "timestamp" : date_time,
        }))


    print("*"*80, "\nSession List: ", session['submitted'], "\n","*"*80,"\n")
    return redirect('/')

@app.route('/destroy_session', methods=['POST'])
def destroy_session():
    session.clear()
    session['attempts'] = -1
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)