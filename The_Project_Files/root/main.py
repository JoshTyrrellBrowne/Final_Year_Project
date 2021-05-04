from flask import Flask, redirect, url_for, render_template, request, session, flash
from __init__ import create_app, db


# THIS IS THE FILE TO RUN THE FLASK WEB APPLICATION

app = create_app()

if __name__ == "__main__":
    #db.create_all()  # this creates the database if one does not yet exist
    app.run(debug=True)



