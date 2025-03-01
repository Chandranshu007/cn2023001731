from flask import Flask, request, redirect, url_for, render_template, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages

# Path to the Excel file
EXCEL_FILE = "registered_users.xlsx"

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = pd.DataFrame([{
            "First Name": firstname,
            "Last Name": lastname,
            "Email": email,
            "Password": password
        }])

        try:
            df_existing = pd.read_excel(EXCEL_FILE)
            df_updated = pd.concat([df_existing, new_user], ignore_index=True)
        except FileNotFoundError:
            df_updated = new_user

        df_updated.to_excel(EXCEL_FILE, index=False)

        flash("Registration Successful!", "success")
        return redirect(url_for("home"))  # ✅ Redirect to home.html

    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html")  # ✅ Load home.html after registration

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)