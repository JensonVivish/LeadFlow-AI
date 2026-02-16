from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# -------------------------------
# EMAIL CONFIG (Update These)
# -------------------------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = "#your email"
app.config["MAIL_PASSWORD"] = "#app password"

app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

mail = Mail(app)


# -------------------------------
# ROUTE: CHATBOT UI
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def chatbot():

    if request.method == "POST":
        try:
            data = request.get_json()

            if not data:
                return jsonify({
                    "status": "error",
                    "message": "No valid JSON received."
                })

            # Extract Lead Info
            name = data.get("name")
            phone = data.get("phone")
            email = data.get("email")
            service = data.get("service")
            message_text = data.get("message")

            # -------------------------------
            # PREMIUM EMAIL TEMPLATE
            # -------------------------------
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
              <style>
                body {{
                  font-family: Arial, sans-serif;
                  background-color: #f4f6f8;
                  padding: 20px;
                }}

                .container {{
                  max-width: 600px;
                  margin: auto;
                  background: white;
                  border-radius: 14px;
                  overflow: hidden;
                  box-shadow: 0px 6px 25px rgba(0,0,0,0.12);
                }}

                .header {{
                  background: linear-gradient(90deg, #0284c7, #38bdf8);
                  padding: 20px;
                  text-align: center;
                  color: white;
                  font-size: 20px;
                  font-weight: bold;
                }}

                .content {{
                  padding: 25px;
                }}

                .lead-box {{
                  background: #f9fafb;
                  border: 1px solid #e5e7eb;
                  border-radius: 12px;
                  padding: 18px;
                  margin-top: 15px;
                }}

                .lead-item {{
                  margin: 10px 0;
                  font-size: 14px;
                }}

                .lead-item strong {{
                  color: #0284c7;
                }}

                .footer {{
                  text-align: center;
                  padding: 15px;
                  font-size: 12px;
                  color: gray;
                  background: #f3f4f6;
                }}
              </style>
            </head>

            <body>
              <div class="container">
                <div class="header">
                  📩 New Lead Received — LeadFlow AI
                </div>

                <div class="content">
                  <p>Hello Team,</p>
                  <p>A new customer inquiry has been submitted:</p>

                  <div class="lead-box">
                    <div class="lead-item"><strong>👤 Name:</strong> {name}</div>
                    <div class="lead-item"><strong>📞 Phone:</strong> {phone}</div>
                    <div class="lead-item"><strong>📧 Email:</strong> {email}</div>
                    <div class="lead-item"><strong>🛠 Service:</strong> {service}</div>
                    <div class="lead-item"><strong>📝 Message:</strong><br>{message_text}</div>
                  </div>

                  <p>Please contact the customer soon.</p>
                </div>

                <div class="footer">
                  LeadFlow AI — Smart CRM Assistant
                </div>
              </div>
            </body>
            </html>
            """

            # -------------------------------
            # SEND EMAIL
            # -------------------------------
            msg = Message(
                subject="📩 New Lead Received — LeadFlow AI",
                recipients=["#recipient_email_id"]
            )

            msg.html = html_body
            mail.send(msg)

            return jsonify({
                "status": "success",
                "message": "Lead submitted successfully!"
            })

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            })

    return render_template("index.html")


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":

    app.run(debug=True)
