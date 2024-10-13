from flask import Flask, render_template, jsonify, request
import requests
import time
from quality_check import check_quality
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env file

app = Flask(__name__)

# Initialize with your existing services
services = []

def send_email(service_url, response_time):
    sender_email = os.getenv("EMAIL_USER")
    receiver_email = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Amazing Service Quality Alert"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Amazing service quality detected!
    Service: {service_url}
    Response Time: {response_time} seconds
    """

    html = f"""\
    <html>
      <body>
        <h2>Amazing Service Quality Alert</h2>
        <p>An amazing service quality has been detected:</p>
        <ul>
          <li><strong>Service:</strong> {service_url}</li>
          <li><strong>Response Time:</strong> {response_time} seconds</li>
        </ul>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent successfully for {service_url}")
    except Exception as e:
        print(f"Failed to send email for {service_url}. Error: {str(e)}")


def check_services():
    results = []
    for service in services:
        start_time = time.time()
        try:
            response = requests.get(service, timeout=10)
            end_time = time.time()
            total_time = end_time - start_time
            service_quality = check_quality(response.status_code, total_time)
            results.append({
                "url": service,
                "status_code": response.status_code,
                "response_time": f"{total_time:.4f}",
                "quality": service_quality
            })
            # if service_quality == "Amazing":
            #     send_email(service, f"{total_time:.4f}")
        except requests.RequestException as e:
            results.append({
                "url": service,
                "status_code": "Error",
                "response_time": "N/A",
                "quality": "Error"
            })
    return results

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    return jsonify(check_services())

@app.route('/add_service', methods=['POST'])
def add_service():
    new_service = request.json.get('url')
    if new_service and new_service not in services:
        services.append(new_service)
        return jsonify({"success": True, "message": "Service added successfully"})
    elif new_service in services:
        return jsonify({"success": False, "message": "Service already exists"})
    else:
        return jsonify({"success": False, "message": "Invalid service URL"})

if __name__ == '__main__':
    app.run(debug=True)
