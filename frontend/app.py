from genericpath import exists
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.utils import secure_filename
import hashlib
import os
import re
from os import path
import pathlib
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import subprocess
from os.path import join
import os.path
import pickle
# from difflib import SequenceMatcher
import cv2
import demo
import numpy as np
app = Flask(__name__)
app.secret_key = "123"

con = sqlite3.connect("database.db")
con.execute("create table if not exists customer(pid integer primary key,name text,address text,contact integer,mail text)")
con.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(
            "select * from customer where name=? and mail=?", (name, password))
        data = cur.fetchone()

        if data:
            session["name"] = data["name"]
            session["mail"] = data["mail"]
            return redirect("customer")
        else:
            flash("Username and Password Mismatch", "danger")
    return redirect(url_for("index"))


@app.route('/customer', methods=["GET", "POST"])
def customer():
    return render_template("customer.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            address = request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("insert into customer(name,address,contact,mail)values(?,?,?,?)",
                        (name, address, contact, mail))
            con.commit()
            flash("Record Added  Successfully", "success")
        except:
            flash("Error in Insert Operation", "danger")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route('/delete/')
def delete():
    stringval = open('code/file.txt').read()
    if os.path.exists("./media/"+stringval):
        os.remove("./media/"+stringval)
    else:
        pass
    return render_template('del.html')


@app.route('/check/', methods=['POST'])
def check_files():
    # Read the uploaded file
    uploaded_file = request.files['file1']

    if not os.path.exists('temp'):
        os.makedirs('temp')

    # Save the uploaded file to the SQLite database
    conn = sqlite3.connect('temp.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO temp_files (file_data)
        VALUES (?)
    ''', (uploaded_file.read(),))

    temp_file_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # Use the model to make a prediction
    with open('code/rf_model.pkl', 'rb') as model_file:
        rfc = pickle.load(model_file)

    # Load the saved file from the SQLite database
    conn = sqlite3.connect('temp.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT file_data
        FROM temp_files
        WHERE id = ?
    ''', (temp_file_id,))

    file_data = cursor.fetchone()[0]

    conn.close()

    # Write the file data to a temporary file
    file_path = 'temp/temp_image.jpg'
    with open(file_path, 'wb') as file:
        file.write(file_data)

    # Load the saved file using OpenCV
    image = cv2.imread(file_path)
    features = []

    # Example: extract the average color of the image
    average_color = np.mean(image, axis=(0, 1))
    features.extend(average_color)

    # Convert the features into a numerical format
    features = np.array(features).reshape(1, -1)

    prediction = rfc.predict(features)

    if prediction == 0:
        # File is benign
        # ...
        return print("File is benign")
    else:
        # File is malware
        return print("File is malware")


if __name__ == '__main__':
    app.run(debug=True)
