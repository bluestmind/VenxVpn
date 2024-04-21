from time import sleep
from urllib import response
from flask import Flask, make_response, render_template, request, session , redirect,url_for,jsonify
from flask_cors import CORS
import settings
import vpnscraper
from database import UserDatabase
from vpnscraper import *
from datetime import datetime, timedelta
from checking import handle_usdt
from settings import *
import re
import os
from flask_sslify import SSLify
import paymentation as PAY
import mail
import subprocess
app = Flask(__name__)
CORS(app, resources={r'*': {'origins': '*'}})
app.secret_key = "osdfsdfsdfsd"

user_db = UserDatabase()
user_db.create_table()


@app.route('/')
def hello_world():
    return render_template("VenXlanding.html")


@app.route('/receive_price', methods=['POST'])
def receive_price():
    data = request.get_json()
    price = data['price']
    duration = data.get('duration')
    user_email = data.get('user_email')
    referral_code = data.get('referral_code')
    session['price'] = price
    session['duration'] = duration
    session['user_email'] = user_email
    session['referral_code'] = referral_code
    print("user email",user_email)
    print("user referral_code", referral_code)
    print("Received price:", price)
    print(f"Received duration: {duration}")

    return 'Price received successfully'



def is_valid_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(email_pattern, email):
        return True
    else:
        return False
#

@app.route('/payment', methods=['POST'])
@app.route('/payment/<flag>', methods=['POST'])
def payment(flag=None):
    if flag is None:
        try:
            email = request.form.get('email')
            sleep(0.2)
            if not is_valid_email(email):
                raise ValueError(f"The email '{email}' is invalid.")
            wallet_address = request.form.get('wallet-address')
            session['wallet_address'] = wallet_address
            price = session['price']
            session['email']= email
            duration = session['duration']
            current_time = datetime.now()
            expire_day = current_time + timedelta(days=1)
            if duration.lower() == "1 year":
                expire_day = current_time + timedelta(days=365)
            elif duration.lower() == "6 months":
                expire_day = current_time + timedelta(days=180)
            elif duration.lower() == "monthly":
                expire_day = current_time + timedelta(days=30)
            expire_day = expire_day.strftime("%Y-%m-%d")

            print("Received Data:")
            print("Email:", email)
            print("Wallet Address:", wallet_address)
            print("Received price:", price)
            print("Expire day:", expire_day)
            trackId = 0
            try:
                trackId = session['track']
            except:
                trackId = 0
            if(trackId==0):
                trackId , payLink = PAY.BindPay(price)
                session['track']=trackId
                return redirect(payLink)
            else:
                if(PAY.TrackPay(trackId)==False):
                    trackId, payLink = PAY.BindPay(price)
                    session['track'] = trackId
                    return redirect(payLink)
                else:
                    return redirect("/receive_data")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("error.html", error=str(e))
    else:
        try:
            data = request.get_json()
            price = data['price']
            duration = data.get('duration')
            user_email = data.get('user_email')
            referral_code = data.get('referral_code')
            session['price'] = price
            session['duration'] = duration
            session['user_email'] = user_email
            session['referral_code'] = referral_code
            sleep(0.2)
            wallet_address = "safadsfsdf"
            session['wallet_address'] = wallet_address

            session['email'] = user_email
            duration = session['duration']
            current_time = datetime.now()
            expire_day = current_time + timedelta(days=1)
            if duration.lower() == "1 year":
                expire_day = current_time + timedelta(days=365)
            elif duration.lower() == "6 months":
                expire_day = current_time + timedelta(days=180)
            elif duration.lower() == "monthly":
                expire_day = current_time + timedelta(days=30)
            expire_day = expire_day.strftime("%Y-%m-%d")

            print("Received Data:")
            print("Email:", user_email)
            print("Wallet Address:", wallet_address)
            print("Received price:", price)
            print("Expire day:", expire_day)

            trackId = session.get('track', 0)
            if trackId == 0:
                trackId, payLink = PAY.BindPay(price)
                session['track'] = trackId
                print(1)
                return redirect(payLink)
            else:
                if not PAY.TrackPay(trackId):
                    trackId, payLink = PAY.BindPay(price)
                    session['track'] = trackId
                    print(2)
                    return redirect(payLink)
                else:
                    return redirect("/receive_data")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render_template("error.html", error=str(e))

import random

@app.route('/receive_data', methods=['GET'])
def receive_data():
    try:
        trackId = 0
        try:
            trackId = session['track']
        except:
            trackId = 0
        if (trackId == 0):
            return render_template("invalid.html")
        print("its ok other datas in the sessions")
        email = session.get('email')
        if not email:
            return render_template("invalid.html")

        wallet_address =session['wallet_address']
        if not wallet_address:
            print("no wallet address entered")
            return render_template("invalid.html")

        price = session.get('price')
        if not price:
            print("no price entered")
            return render_template("invalid.html")

        duration = session.get('duration')
        if not duration:
            print("no duration entered")
            return render_template("invalid.html")
        current_time = datetime.now()
        expire_day = current_time + timedelta(days=1)
        if duration.lower() == "1 year":
            expire_day = current_time + timedelta(days=365)
            x =365
        elif duration.lower() == "6 months":
            expire_day = current_time + timedelta(days=180)
            x = 180
        elif duration.lower() == "monthly":
            expire_day = current_time + timedelta(days=30)
            x = 30
        expire_day = expire_day.strftime("%Y-%m-%d")
        random_number = random.randint(10000, 99999)
        print(random_number)
        user_email = f"{email}{random_number}"
        print(email)
        if not (trackId==0):
            if (trackId == 0):
                return render_template("invalid.html")
            else:
                if PAY.TrackPay(trackId=trackId) and session["track"] != 0:
                    print("Payment approved")
                    session["track"] = 0
                    # result = subprocess.run(['python', 'vpnscraper.py', user_email, expire_day, 'note', str(settings.user_name), str(settings.password)], stdout=subprocess.PIPE, text=True)
                    z,config=DEF_CREATE_USER(user_email,x)
                    sub_link = "https://panel.venxvp.com:8443{}".format(z)
                    subject, content = settings.TransactionSuccessEmail(email, config, wallet_address, expire_day, price,sub_link)
                    mail.send_html_email(subject, content, email)


                    return render_template("done.html", config=config, email=email, txid=trackId, wallet_address=wallet_address, price=price, expire_day=expire_day, sub_link=sub_link)
                else:
                    print("payment is wrong")
                    return render_template("invalid.html")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("error.html", error=str(e))



@app.route('/hardin_007/<user>', methods=['GET', 'POST'])
def test(user):
    print("dsfsdfsdfsd")
    email = "hardinadamstm@gmail.com"
    random_number = random.randint(10000, 99999)
    print(random_number)
    user_email = f"{user}{random_number}"
    z, config = DEF_CREATE_USER(user_email, 30)
    sub_link = "https://panel.venxvp.com:8443{}".format(z)
    subject, content = settings.TransactionSuccessEmail(email, config, "wallet_address", "expire_day", "price", sub_link)
    mail.send_html_email(subject, content, email)
    subject, content = settings.TransactionSuccessEmail(email, config, "wallet_address", "2024-03-31", 20, sub_link)
    mail.send_html_email(subject, content, email)
    session["track"] = 0
    return render_template("done.html", config=config, email=email, txid="trackId",wallet_address="wallet_address", price=20, expire_day="2024-03-31", sub_link=sub_link)


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    if 'logged_in' in session and session['logged_in']:
        email = session['email']
        existing_user = user_db.get_user_by_email(email)
        if existing_user:
            referral_code = user_db.get_referral_code_by_email(email)
            trx_amount = "120 TRX"
            total_profit = "12,364 (TRX)"
            profit_amount = "+2,541 (TRX)"
            member_amount = "+45 Members"
            return render_template('dashboard.html', trx_amount=trx_amount, referral_code=referral_code,
                                   total_profit=total_profit, profit_amount=profit_amount, member_amount=member_amount)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect(url_for('login'))


import hashlib


def generate_random_referral_code(full_name, email):
    data = full_name + email
    hashed_data = hashlib.md5(data.encode()).hexdigest()
    referral_code = hashed_data[:6].upper()

    return referral_code


@app.route('/signup_form', methods=['POST'])
def signup_form():
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    if request.form['referral_code']:
        user_invite_by = request.form['referral_code']
    else:
        user_invite_by = None
    existing_user = user_db.get_user_by_email(email)

    if existing_user:
        return render_template('signup.html', error_message="User with this email already exists.",
                               script="displayModal()")

    referral_code = generate_random_referral_code(full_name, email)

    user_db.insert_user(full_name, email, password, referral_code, user_invite_by)

    trx_amount = "120 TRX"
    referral_code = user_db.get_referral_code_by_email(email)
    total_profit = "12,364 (TRX)"
    profit_amount = "+2,541 (TRX)"
    member_amount = "+45 Members"
    session['logged_in'] = True
    session['email'] = email
    return render_template('dashboard.html', trx_amount=trx_amount, referral_code=referral_code,
                           total_profit=total_profit, profit_amount=profit_amount, member_amount=member_amount)


@app.route('/admin_panel', methods=['GET'])
def admin_panel():
    role = session.get('role')
    if role != 'admin':
        return render_template("error.html", error="You are not authorized to access this page.")
    all_tickets = user_db.get_all_tickets()
    open_tickets = user_db.get_open_tickets()

    return render_template("adminpanel.html", open_tickets=open_tickets,all_tickets=all_tickets)


@app.route('/submit_response', methods=['POST'])
def submit_response():
    # Extract data from the request
    data = request.json
    email = data.get('userEmail')
    ticket_id = data.get('ticketId')
    response = data.get('response')

    print("Ticket ID:", ticket_id)
    print("Response:", response)
    user_db.update_ticket_response(ticket_id, response)
    # Return a JSON response indicating success
    subject = f"Ticket response from Venx,Ticket id: {ticket_id}"
    content = response
    mail.send_html_email(subject, content, email)
    user_db.update_ticket_status_by_id(ticket_id,"closed")
    return jsonify({'message': 'Response submitted successfully'}), 200

@app.route('/users_response', methods=['POST'])
def users_response():
    # Extract data from the request
    data = request.json
    email = data.get('userEmail')
    role = data.get('userRole')
    print("role:", role)
    user_db.update_role_by_email(email,role)
    return jsonify({'message': 'Response submitted successfully'}), 200

@app.route('/users')
def users():
    if session['role'] == "admin":
        all_users = user_db.get_all_users()
        return render_template('users.html',all_users=all_users)
    else:
        return render_template("VenXlanding.html")

@app.route('/login_form', methods=['POST'])
def login_form():
    email = request.form['email']
    password = request.form['password']
    existing_user = user_db.get_user_by_email(email)
    check_password = user_db.verify_password(email,password)
    print(check_password)
    role= user_db.get_role_by_email(email)
    if check_password:
        if role == 'admin':
            session['role'] = 'admin'
            return redirect(url_for('admin_panel'))
        if existing_user:
            referral_code = user_db.get_referral_code_by_email(email)
            print("here ?")
            session['logged_in'] = True
            session['email'] = email
            trx_amount = "120 TRX"
            total_profit = "12,364 (TRX)"
            profit_amount = "+2,541 (TRX)"
            member_amount = "+45 Members"
            user_email = ["Iman"]
            sliders_data = []

            for email in user_email:
                sub_link, total_usage, expire,days_remaining = vpnscraper.getusage(
                    email)

                sliders_data.append({
                    'id': len(sliders_data) + 1,
                    'total_usage': total_usage,
                    'current_plan': 'Sapphire',
                    'expires_on': expire,
                    'days_left': int(days_remaining),
                    'sublink': sub_link
                })

            return render_template('dashboard.html', trx_amount=trx_amount, referral_code=referral_code,
                                   total_profit=total_profit, profit_amount=profit_amount, member_amount=member_amount,sliders=sliders_data,user_email=email)
        else:
            return render_template('login.html', error_message="User not found",
                                   script="displayModal()")
    else:
        return render_template('login.html', error_message="password is wrong",
                               script="displayModal()")




@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        email = session.get('email')
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if user_db.verify_password(email, current_password):

            if new_password == confirm_password:

                user_db.update_password_by_email(email, new_password)
                return redirect(url_for('dashboard'))
            else:
                return "New password and confirm password do not match."
        else:
            return "Current password is incorrect."

    return render_template('change_password.html')


@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        email = session['email']
        existing_user = user_db.get_user_by_email(email)
        if existing_user:
            referral_code = user_db.get_referral_code_by_email(email)
            trx_amount = "120 TRX"
            total_profit = "12,364 (TRX)"
            profit_amount = "+2,541 (TRX)"
            member_amount = "+45 Members"
            return render_template('dashboard.html', trx_amount=trx_amount, referral_code=referral_code,
                                   total_profit=total_profit, profit_amount=profit_amount, member_amount=member_amount)
    else:
        return redirect(url_for('login'))

import uuid
@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    # Handle form submission here
    subject = request.form['subject']
    description = request.form['description']
    email = request.form['user_email']
    ticket_number = str(uuid.uuid4())
    print(email)
    print(subject)
    print(description)
    user_db.insert_ticket_by_email(email,subject,description,ticket_number)
    # Process the ticket (e.g., save to database)
    # Replace this with your actual ticket processing logic

    return 'Success'  # or return jsonify({'message': 'Success'}) if you prefer JSON response


if __name__ == '__main__':
    user_db.create_table()
    sslify = SSLify(app)
    app.run(host='0.0.0.0', port=8080, debug=True)
