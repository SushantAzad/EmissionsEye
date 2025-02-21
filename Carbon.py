import mysql.connector

def checktable(table):     # Check if the table exists
    sqr.execute(f"SHOW TABLES LIKE '{table}'")
    return bool(sqr.fetchone())

# Database Connection
mycon = mysql.connector.connect(host="localhost", user="root", passwd="My!nst@_1136", database="emissionseye")
sqr = mycon.cursor()

loggedIn = False

if checktable("profile"):
    choice0 = int(input("1. Login\n2. Create New Profile\n"))
    if choice0 == 1:
        email = input("Enter your email:\n")
        password = input("Enter your password:\n")
        sqr.execute("SELECT email, password FROM profile;")
        for row in sqr.fetchall():
            if row[0] == email and row[1] == password:
                loggedIn = True
    elif choice0 == 2:
        name = input("Enter your name:\n")
        email = input("Enter your email:\n")
        mob = input("Enter your mobile number:\n")
        password = input("Enter your password:\n")
        sqr.execute(f"INSERT INTO profile VALUES('{name}','{email}','{mob}','{password}');")
        mycon.commit()
        loggedIn = True
        print("User Profile created!\n")
else:
    name = input("Enter your name:\n")
    email = input("Enter your email:\n")
    mob = input("Enter your mobile number:\n")
    password = input("Enter your password:\n")
    sqr.execute("CREATE TABLE profile(Name VARCHAR(30), Email VARCHAR(30), Mobile VARCHAR(10), Password VARCHAR(50));")
    sqr.execute(f"INSERT INTO profile VALUES('{name}','{email}','{mob}','{password}');")
    mycon.commit()
    loggedIn = True
    print("User Profile created!\n")

usage = [0] * 12
while loggedIn:
    choice1 = int(input("1. Transportation\n2. Energy Usage\n3. Purchases & Waste\n4. Offsets & Reduction\n5. Submit\n"))

    if choice1 == 1:
        while choice1 == 1:
            choice2 = int(input("1. Car\n2. Public Transport\n3. Flight\n4. Next Category\n"))
            if choice2 == 1:
                choice3 = int(input("1. Petrol\n2. Diesel\n3. EV\n"))
                carDistance = int(input("Enter distance travelled by Car:\n"))
                factors = [0.20, 0.25, 0.05]
                usage[0] = carDistance * factors[choice3 - 1]
            elif choice2 == 2:
                choice4 = int(input("1. Bus\n2. Train\n3. Metro\n"))
                pubDistance = int(input("Enter distance travelled by Public Transport:\n"))
                factors = [0.07, 0.05, 0.04]
                usage[1] = pubDistance * factors[choice4 - 1]
            elif choice2 == 3:
                choice5 = int(input("1. Short haul\n2. Long haul\n"))
                noOfFlights = int(input("Enter no. of flights taken:\n"))
                factors = [250, 1000]
                usage[2] = noOfFlights * factors[choice5 - 1]
            elif choice2 == 4:
                choice1 = 2

    elif choice1 == 2:
        while choice1 == 2:
            choice6 = int(input("1. Electricity Consumption\n2. LPG Usage\n3. Heating (Natural Gas)\n4. Next Category\n"))
            values = [0.5, 2.98, 1.85]
            input_values = [int(input(f"Enter the amount (in appropriate units) for {item}:\n")) for item in ["Electricity (kWh)", "LPG (kg)", "Natural Gas (m^3)"]]
            usage[3:6] = [input_values[i] * values[i] for i in range(3)]
            if choice6 == 4:
                choice1 = 3

    elif choice1 == 3:
        while choice1 == 3:
            choice7 = int(input("1. Clothing\n2. Electronics\n3. Plastic Waste\n4. Food Waste\n5. Next Category\n"))
            values = [50, 70, 200, 2.5, 0.9]
            if choice7 == 1:
                usage[6] = int(input("Enter the No. of clothing items:\n")) * values[0]
            elif choice7 == 2:
                mobiles = int(input("Enter the no. of Mobiles:\n"))
                laptops = int(input("Enter the no. of Laptops:\n"))
                usage[7] = mobiles * values[1] + laptops * values[2]
            elif choice7 == 3:
                usage[8] = int(input("Enter the amount of plastic waste (in kg):\n")) * values[3]
            elif choice7 == 4:
                usage[9] = int(input("Enter the amount of food waste (in kg):\n")) * values[4]
            elif choice7 == 5:
                choice1 = 4

    elif choice1 == 4:
        while choice1 == 4:
            choice8 = int(input("1. Tree Planting\n2. Renewable Energy\n3. Next Category\n"))
            values = [-20, -0.5]
            if choice8 == 1:
                usage[10] = int(input("Enter the no. of trees you planted:\n")) * values[0]
            elif choice8 == 2:
                usage[11] = int(input("Enter the no. of kWh renewable energy generated:\n")) * values[1]
            elif choice8 == 3:
                choice1 = 5

    elif choice1 == 5:
        total = round(sum(usage), 2)
        print(f"Total Carbon Emissions: {total} kg\n")
        sqr.execute("SELECT CURRENT_TIMESTAMP;")
        timestamp = sqr.fetchone()[0]
        sqr.execute("INSERT INTO history (Date_Time, Total) VALUES (%s, %s)", (timestamp, total))
        mycon.commit()
        print("Data saved successfully!\n")
        break
