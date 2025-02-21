def checktable(table):     #to check if the table exists already
    sqr.execute(f"show tables like '{table}'")
    result = sqr.fetchone()
    if result:
        return True
    else:
        return False

import mysql.connector          #setup connection
mycon = mysql.connector.connect(host = "localhost",user="root",passwd="9617",database="emissionseye")
sqr = mycon.cursor()

loggedIn = False
if(checktable("profile")):
    choice0 = int(input("1.Login\n2.Create New Profile\n"))
    if(choice0==1):
        email = input("Enter your email:\n")
        password = input("Enter your password:\n")
        str0 = "select email, password from profile;"
        sqr.execute(str0)
        userdata = sqr.fetchall()
        for i1 in userdata:
            if (i1[0] == email) and (i1[1] == password):
                loggedIn = True
    elif(choice0 == 2):
        name = input("Enter your name:\n")
        email = input("Enter your email:\n")
        mob = input("Enter your mobile number:\n")
        password = input("Enter your password\n")
        str2 = f"insert into profile values('{name}','{email}','{mob}','{password}');"
        sqr.execute(str2)
        mycon.commit()
        loggedIn = True
        print("User Profile created!\n")
else:
    name = input("Enter your name:\n")
    email = input("Enter your email:\n")
    mob = input("Enter your mobile number:\n")
    password = input("Enter your password\n")
    str1 = "create table profile(Name varchar(30),Email varchar(30), Mobile varchar(10),Password varchar(50));"
    sqr.execute(str1)
    str2 = f"insert into profile values('{name}','{email}','{mob}','{password}');"
    sqr.execute(str2)
    mycon.commit()
    loggedIn = True
    print("User Profile created!\n")

usage = [0,0,0,0,0,0,0,0,0,0,0,0] 
while(loggedIn):
    choice1 = int(input("1.Transportation\n2.Energy Usage\n3.Purchases & Waste\n4.Offsets & Reduction\n5.Submit\n"))

    if(choice1==1):
        while(choice1==1):
            choice2 = int(input("1.Car\n2.Public Transport\n3.Flight\n4.NextCat\n"))
            if(choice2 == 1):
                choice3 = int(input("1.Petrol\n2.Deisel\n3.EV\n"))
                carDistance = int(input("Enter distance travelled by Car:\n"))
                if(choice3 == 1):
                    usage[0] = carDistance*0.20
                elif(choice3 == 2):
                    usage[0] = carDistance*0.25
                elif(choice3 == 3):
                    usage[0] = carDistance*0.05
            elif(choice2==2):
                choice4 = int(input("1.Bus\n2.Train\n3.Metro\n"))
                pubDistance = int(input("Enter distance travelled by Public Transport:\n"))
                if(choice4 == 1):
                    usage[1] = pubDistance*0.07
                elif(choice4 == 2):
                    usage[1] = pubDistance*0.05
                elif(choice4 == 3):
                    usage[1] = pubDistance*0.04
            elif(choice2==3):
                choice5 = int(input("1.Short haul\n2.Long haul\n"))
                noOfFlights = int(input("Enter no. of flights taken:\n"))
                if(choice5==1):
                    usage[2] = noOfFlights*250
                elif(choice5==2):
                    usage[2] = noOfFlights*1000
            elif(choice2==4):
                choice1 = 2
    
    elif(choice1==2):
        while(choice1==2):
            choice6 = int(input("1.Electricity Consumption\n2.LPG Usage\n3.Heating (Natural Gas)\n4.NextCat\n"))
            if(choice6==1):
                kwh = int(input("Enter the No. of kWh electricity used:\n"))
                usage[3] = kwh*0.5
            elif(choice6==2):
                lpg = int(input("Enter the amount of LPG used (in kg):\n"))
                usage[4] = lpg*2.98
            elif(choice6==3):
                gas = int(input("Enter the amount of Natural Gas used (in m^3):\n"))
                usage[5] = gas*1.85
            elif(choice6==4):
                choice1 = 3  

    elif(choice1==3):
        while(choice1==3):
            choice7 = int(input("1.Clothing\n2.Electronics\n3.Plastic Waste\n4.Food WAste\n5.NextCat\n"))
            if(choice7==1):
                noOfClothes = int(input("Enter the No. of clothing items:\n"))
                usage[6] = noOfClothes*50
            elif(choice7==2):
                noOfMobiles = int(input("Enter the no. of Mobiles:\n"))
                noOfLaptops = int(input("Enter the no. of Laptops:\n"))
                usage[7] = noOfMobiles*70 + noOfLaptops*200
            elif(choice7==3):
                plasticWaste = int(input("Enter the amount of plastic waste (in kg):\n"))
                usage[8] = plasticWaste*2.5
            elif(choice7==4):
                foodWaste  = int(input("Enter the amount of food waste (in kg):\n"))
                usage[9] = foodWaste*0.9
            elif(choice7==5):
                choice1 = 4

    elif(choice1==4):
        while(choice1==4):  
            choice8 = int(input("1.Tree Planting\n2.Renewable Energy\n3.NextCat\n"))
            if(choice8==1):
                noOfTrees = int(input("Enter the no. of trees you planted:\n"))
                usage[10]  =  noOfTrees*(-20)
            elif(choice8==2):
                kwh2 = int(input("Enter the no. of kWh renewable energy generated:\n"))
                usage[11]  =  kwh2*(-0.5)
            elif(choice8==3):
                choice1=5
    
    elif(choice1==5):
        total = 0
        for i in usage:
            total = total+i
        total = str(round(float(total),2))
        print(f"{total}\n")
        sqr.execute("select current_timestamp;")
        timestamp = sqr.fetchone()
        sqr.execute(f"create table `{timestamp[0]}`(Category varchar(20),Emission varchar(10));")
        category = ["Car","Public Transport","Flight","Electricity","LPG","Heating (NG)","Clothing","Electronics","Plastic Waste","Food Waste","Tree Planting","Renewable Energy"]
        str3 = f"insert into `{timestamp[0]}` values"
        for i1 in range(0,12):
            str3 = str3 + f"('{category[i1]}','{usage[i1]}')"
            if(i1!=11):
                str3 = str3 + ","
            else:
                str3 = str3 + ";"
        sqr.execute(str3)
        mycon.commit()
        
        if(checktable("history")):
            print("Updating History\n")
        else:
            sqr.execute(f"create table History(Date_Time varchar(20),Total varchar(255));")
        sqr.execute(f"insert into history values('{timestamp[0]}','{total}');")
        mycon.commit()

        print(f"The total amount of Carbon Emissions by you is {total}\n")
        break
