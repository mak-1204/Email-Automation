from datetime import date
import pandas as pd
from automation import send_email  # Your attendance email + graph function

# Google Sheet Details
SHEET_ID = "1WTpnEw8SWukFEwVxB5qjbaeAQk2MrZsWWLC6KLJQ268"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    df = pd.read_csv(url)
    return df

def send_attendance_emails(df):
    today = date.today()
    email_counter = 0

    for _, row in df.iterrows():
            send_email(
                subject=f"[ChampionX] October Attendance Report",
                receiver_email=row["email"],
                name=row["name"],
                level=row["level"],
                Week1=int(row["Week 1"]),
                Week2=int(row["Week 2"]),
                Week3=int(row["Week 3"]),
                Week4=int(row["Week 4"]),
            )
            email_counter += 1

    return f"Total Emails Sent: {email_counter}"

# Execution
df = load_df(URL)
result = send_attendance_emails(df)
print(result)
