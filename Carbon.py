name = input("Enter your name:\n")
email = input("Enter your email:\n")
mob = input("Enter your mobile number:\n")
while(True):
    usage = [0,0,0,0,0,0,0,0,0,0,0,0]
    choice1 = input("1.Transportation\n2.Energy Usage\n3.Purchases & Waste\n4.Offsets & Reduction\n5.Submit\n")
    if(choice1==1):
        while(True):
            choice2 = input("1.Car\n2.Public Transport\n3.Flight\n4.NextCat\n")
            if(choice2 == 1):
                choice3 = input("1.Petrol\n2.Deisel\n3.EV\n")
                carDistance = input("Enter distance travelled by Car:\n")
                if(choice3 == 1):
                    usage[0] = carDistance*0.20
                elif(choice3 == 2):
                    usage[0] = carDistance*0.25
                elif(choice3 == 3):
                    usage[0] = carDistance*0.05
            elif(choice2==2):
                choice4 = input("1.Bus\n2.Train\n3.Metro\n")
                pubDistance = input("Enter distance travelled by Public Transport:\n")
                if(choice4 == 1):
                    usage[0] = usage[0] + pubDistance*0.07
                elif(choice4 == 2):
                    usage[0] = usage[0] + pubDistance*0.05
                elif(choice4 == 3):
                    usage[0] = usage[0] + pubDistance*0.04
            elif(choice2==3):
                choice5 = input("1.Short haul\n2.Long haul\n")
                noOfFlights = input("Enter no. of flights taken:\n")
                if(choice5==1):
                    usage[0] = usage[0] + noOfFlights*250
                elif(choice5==2):
                    usage[0] = usage[0] + noOfFlights*1000
            elif(choice2==4):
                break