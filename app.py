from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv
import inspect

# Monkey patch inspect if necessary
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec
  
load_dotenv()  # Load environment variables from .env file

posts = requests.get("https://api.npoint.io/dd3927781f4255e907e6").json()

app = Flask('app')

@app.route('/')
def home():
  return render_template("index.html", res = posts)

@app.route('/post/<int:num>')
def get_blog(num):
  for post in posts:
    if num == post["id"]:
      requested_blog = post
  return render_template("post.html", blog = requested_blog)
    
@app.route('/about')
def about():
  return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
  if request.method == "POST":
    data = request.form
    success = True  
    send_email(data["name"], data["email"])
    return render_template("contact.html",success=True)
  return render_template("contact.html",success=False)

def send_email(name, email):
    name = name.capitalize()
    email_subject = "Thank You for Contacting Us"
    email_message = f'''Subject:{email_subject}\n
Hi {name},

Thank you for getting in touch with us! We have received your message and appreciate you taking the time to contact us.

We value your feedback and questions, and we will get back to you as soon as possible. If your inquiry requires immediate attention, please be patient as we strive to provide the best response.

In the meantime, feel free to explore our latest blog posts and updates. We are always here to share knowledge and engage with our community.

Thank you for being a part of our community!

Best regards,
Harshita's Blog ❤️'''

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, email, email_message.encode('utf-8'))


app.run(debug=True)
