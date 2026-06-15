import datetime as dt
import pandas as pd
from random import randint
import smtplib

my_email = "t20940382@gmail.com"
password = "blguxeearbzudiag"

now = dt.datetime.now()
today_month = now.month
today = now.day
##################### Extra Hard Starting Project ######################

birth_data = pd.read_csv("birthdays.csv")
all_birthdays = birth_data.to_dict(orient="records")

for birthday_checker in all_birthdays:
    if birthday_checker["month"] == today_month and birthday_checker["day"] == today:
        with open(f"letter_templates/letter_{randint(1, 3)}.txt") as greeting_file:
            template = greeting_file.read()
        clean_name = birthday_checker["name"].strip()
        new_letter = template.replace("[NAME]", clean_name)
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=birthday_checker["email"],
                msg=f"Subject:Happy Birthday\n\n{new_letter}"
            )



