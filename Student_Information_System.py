import re

emails_passwords = {"123@gmail.com":"123456", "justin@gmail.com":"123456", "rakshan":"123456"}

Student_details = {}

class student:
    def personal_details(self,name,age,city):
        print(f"hi {name} your {age} years old and from {city}") 

    def educational_details(self,std,section,roll_num):
        print(f"your education is {std} {section} section and your Roll number is {roll_num}") 

getdetails = student()


regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
attemps = 0
email_valid = False

while attemps < 5:
    email = input("Enter your email:") 
    password = input("Enter your password:")     
    if re.match(regex, email) and emails_passwords.get(email) == password:
        email_valid = True
        break
    else:
        print(f"Invalid email or password. Attempts remaining: {4 - attemps}")
    attemps += 1 

if email_valid:
    print(f"Welcome {email} ")

    print("PERSONAL DETAILS")
    name = input("Enter your name:")
    age = int(input("Enter your age:"))
    city = input("Enter Your city:")


    print("Educational Details")
    std = input("Which class are you:")
    section = input("Which Section are you?:")
    roll_num = input("What is your roll number?:")

  
    Student_details[email] = { "name": name,
    "age": age,
    "city": city,
    "class": std,
    "section": section,
    "roll_num": roll_num
    }

    getdetails.personal_details(name,age,city)
    getdetails.educational_details(std,section,roll_num)

    print(Student_details)


else:
    print("Wrong email. Out of attempts.")
    




    