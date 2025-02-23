from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"


try:
    mycon = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Lucky@123",
        database="emissionseye",
        auth_plugin="mysql_native_password"
    )
    sqr = mycon.cursor()
except mysql.connector.Error as err:
    print(f" MySQL Connection Error: {err}")
    exit(1)  


def create_tables():
    sqr.execute("""CREATE TABLE IF NOT EXISTS profile (
        Name VARCHAR(30), 
        Email VARCHAR(50) PRIMARY KEY, 
        Password VARCHAR(50)
    )""")
    
    mycon.commit()


create_tables()


def create_user_table(email):
    table_name = email.replace("@", "_").replace(".", "_")

    sqr.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = sqr.fetchone()

    if not result:  
        sqr.execute(f"DROP TABLE IF EXISTS `{table_name}`")  # 
        sqr.execute(f"""CREATE TABLE `{table_name}` (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Date_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Car FLOAT, PublicTransport FLOAT, Flight FLOAT,
            Electricity FLOAT, LPG FLOAT, Clothing FLOAT, Electronics FLOAT, PlasticWaste FLOAT,
            FoodWaste FLOAT, TreesPlanted FLOAT, RenewableEnergy FLOAT,
            Total FLOAT
        )""")
        mycon.commit()


@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("cover"))


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("cover")) 
    return render_template("index.html")


@app.route("/education")
def education():
    return render_template("education.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/cover")
def cover():
    return render_template("cover.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    sqr.execute("SELECT Email FROM profile WHERE Email=%s AND Password=%s", (email, password))
    user = sqr.fetchone()

    if user:
        session["email"] = email  
        return redirect(url_for("dashboard")) 
    else:
        return " Invalid Email or Password. <a href='/cover'>Try again</a>"

@app.route("/signup", methods=["POST"])
def signup():
    try:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        print(f"Received signup data: name={name}, email={email}, password={password}")  

        
        sqr.execute("SELECT Email FROM profile WHERE Email=%s", (email,))
        existing_user = sqr.fetchone()

        if existing_user:
            return " Email already registered. <a href='/cover'>Login instead</a>"

        
        sqr.execute("INSERT INTO profile (Name, Email, Password) VALUES (%s, %s, %s)", 
                    (name, email, password))
        mycon.commit()

        create_user_table(email)  

        session["email"] = email 
        print(f"✅ User {email} registered successfully!")  

        return redirect(url_for("dashboard"))  

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}") 
        return " Database Error. Please try again."

    except Exception as e:
        print(f" General Error: {e}")  
        return f" Something went wrong. Please try again. Error: {e}"


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if "email" not in session:
        return redirect(url_for("cover")) 

    email = session["email"]
    table_name = email.replace("@", "_").replace(".", "_")  

    if request.method == "POST":
        
        usage = [0] * 12

        
        if "car_distance" in request.form:
            fuel_type = request.form["fuel_type"]
            car_distance = float(request.form["car_distance"])
            fuel_emission = {"petrol": 0.20, "diesel": 0.25, "CNG": 0.10}
            usage[0] = car_distance * fuel_emission.get(fuel_type, 0)

      
        if "public_distance" in request.form:
            transport_type = request.form["transport_type"]
            transport_emission = {"bus": 0.07, "train": 0.05, "metro": 0.04}
            usage[1] = float(request.form["public_distance"]) * transport_emission.get(transport_type, 0)

      
        if "flight_distance" in request.form:
            flight_distance = float(request.form["flight_distance"])
            flight_type = request.form["flight_type"]
            usage[2] = flight_distance * (250 if flight_type == "short-haul" else 1000)

        
        categories = ["electricity", "lpg", "natural_gas", "clothes", "electronics", "plastic_waste", "food_waste", "trees_planted", "renewable_energy"]
        emission_factors = [0.5, 2.98, 1.85, 50, 70, 2.5, 0.9, -20, -0.5]

        for i, category in enumerate(categories):
            usage[i + 3] = float(request.form.get(category, 0)) * emission_factors[i]

        total_emission = round(sum(usage), 2)

       
        print("Usage values:", usage)
        print("Total emission:", total_emission)
        print("Number of parameters:", len(usage))

       
        sql_query = f"""INSERT INTO `{table_name}` 
        (Car, PublicTransport, Flight, Electricity, LPG, NaturalGas, Clothing, Electronics, PlasticWaste, FoodWaste, TreesPlanted, RenewableEnergy, Total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        print("SQL Query:", sql_query)
        print("Parameters:", usage + [total_emission])

        
        sqr.execute(sql_query, usage + [total_emission])
        mycon.commit()

        return redirect("/result")

    return render_template("calculator.html")




@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("cover"))

if __name__ == "__main__":
    app.run(debug=True)
