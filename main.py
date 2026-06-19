import datetime
import smtplib
import os
import requests
from datetime import datetime as dt


my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

MY_LAT = 14.675461
MY_LONG = 121.114812

iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_data = iss_response.json()

iss_longitude = float(iss_data["iss_position"]["longitude"])
iss_latitude = float(iss_data["iss_position"]["latitude"])

iss_position = (iss_longitude,iss_latitude)


parameters = {
    "lat":MY_LAT,
    "lng":MY_LONG,
    "max_lat": MY_LAT + 0.07,
    "min_lat": MY_LAT - 0.07,
    "max_lng": MY_LONG + 0.07,
    "min_lng": MY_LONG - 0.07,
    "formatted":0
}



print(f"LAT: {parameters["lat"]}")
print(f"LNG: {parameters["lng"]}")

sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
sun_response.raise_for_status()

sun_data = sun_response.json()

sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = dt.now(datetime.UTC).hour
print(f"SUNRISE: {sunrise}")
print(f"SUNSET: {sunset}")
print(f"CURRENT TIME: {time_now}")

#If the ISS is close to my current position
#and it is currently dark
#then send me an email to tell me to look up.
#BONUS: run the code every 60 seconds

if (parameters["max_lat"] >= iss_latitude >= parameters["min_lat"] and parameters["max_lng"] >= iss_longitude >= parameters["min_lng"] and (time_now >= sunset or time_now <= sunrise)):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="kcmsn.ccna@gmail.com",
            msg=f"Subject: ISS IS NEARBY!\n\n"
                f"Look up! The ISS is nearby.\n"
                f"Current location:\n"
                f"Latitude: {iss_latitude}\n"
                f"Longitude: {iss_longitude}\n"
        )
            
