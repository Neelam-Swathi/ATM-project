from flask import Flask,render_template,request
app = Flask(__name__)
accounts = {}
@app.route('/')
def home():
    return render_template('home.html', accounts = accounts)
@app.route('/home')
def home2():
    return render_template('home.html', accounts = accounts)
@app.route('/create',methods = ['POST','GET'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    account_no = request.form.get('acc_no')
    name = request.form.get('name')
    balance = request.form.get('balance')
    if len(account_no) != 10 :
        return render_template('create.html',message = 'Invalid acount number',msg_type = 'error')
    if account_no in accounts:
        return render_template('create.html', message='Account number already exists', msg_type='error')
    if int(balance) < 2000 :
        return render_template('create.html',message = 'Min balance : 2000',msg_type = 'error')
    accounts [account_no] = {'name': name, 'balance': int(balance)}
    message = 'Account created successfully !!'
    return render_template('create.html',message = message,msg_type = 'success')
@app.route('/balance', methods = ['GET','POST'])
def balance():
    if request.method == 'POST':
        account_no = request.form.get('acc_no')
        if account_no in accounts:
            account = accounts[account_no]
            return render_template('balance.html',account = account)
        else:
            return render_template('balance.html',message = 'Account does not exist',msg_type = 'error')

    return render_template('balance.html')
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update.html')

    acc_no = request.form.get('acc_no')
    amount = int(request.form.get('amount'))
    action = request.form.get('action') 

    if acc_no not in accounts:
        return render_template('update.html', message='Account not found', msg_type='error')
    details = accounts[acc_no]
    balance = details['balance']
    if action == 'deposit':
        details['balance'] += amount 
        message = "Deposited Successful !!"  
    elif action == 'withdraw' and balance >= amount :
        details['balance'] -= amount
        message = "Withdraw Successfull !!"   
    else:
        message = "Limit Exceeded"    
    return render_template('update.html', message=message, msg_type='success')
@app.route('/delete',methods = ['POST','GET'])
def delete():
    if request.method == 'POST':
        acc_no = request.form.get('acc_no')
        if acc_no in accounts :
            accounts.pop(acc_no)
            message = "Deleted Successfully !!"
            msg_type = 'success'
        else :
            message = "Account not found"
            msg_type = 'error'
        return render_template('delete.html',message= message, msg_type = msg_type)

    return render_template('delete.html')
app.run(debug = True,port=5003)