import mimetypes
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import matplotlib.pyplot as plt
import smtplib

from dotenv import load_dotenv

PORT=587
EMAIL_SERVER="smtp.gmail.com"


# Load environment variables 
current_dir = Path.cwd()
envars = current_dir / '.env'
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
















print(sender_email, password)

# def send_email(subject, receiver_email, name, level, Week1, Week2, Week3, Week4):
#     # Attendance data
#     weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
#     attendance = [Week1, Week2, Week3, Week4]
#     attendance_percentage = (sum(attendance) / 4) * 100

#     # Generate attendance plot
#     plt.figure(figsize=(6, 4))
#     bars = plt.bar(weeks, attendance, color=["green" if x else "red" for x in attendance])
#     plt.ylim(0, 1.2)
#     plt.title(f"{name}'s Attendance - October")
#     plt.ylabel("Attendance")
#     plt.xticks(rotation=45)
#     plt.yticks([0, 1], ["Absent", "Present"])
#     for bar, value in zip(bars, attendance):
#         plt.text(bar.get_x() + 0.1, bar.get_height() + 0.05, 'Present' if value else 'Absent', color='black')

#     plt.tight_layout()
#     graph_filename = "attendance_graph.png"
#     plt.savefig(graph_filename)
#     plt.close()

#     # Create email
#     msg = EmailMessage()
#     msg['Subject'] = subject
#     msg['From'] = formataddr(("ChampionX", f"{sender_email}"))
#     msg['To'] = receiver_email
#     msg['BCC'] = sender_email

#     # Email text content
#     msg.set_content(
#         f"""
#         Hi {name}, currently you are at {level} level in Toastmasters,

#         This is a mail about your Toastmasters Attendance for the month of October.
#         Your attendance for the month is as follows:

#         Week 1: {"Present" if Week1 == 1 else "Absent"}
#         Week 2: {"Present" if Week2 == 1 else "Absent"}
#         Week 3: {"Present" if Week3 == 1 else "Absent"}
#         Week 4: {"Present" if Week4 == 1 else "Absent"}

#         And your attendance percentage is: {attendance_percentage:.2f}%

#         Thank you for being a part of our club.

#         Regards,
#         Toastmasters ChampionX Team
#         """)

#     # Attach graph
#     with open(graph_filename, "rb") as f:
#         file_data = f.read()
#         msg.add_attachment(file_data, maintype='image', subtype='png', filename=graph_filename)

def send_email(subject, receiver_email, name, level, Week1, Week2, Week3, Week4):
    # Attendance data
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
    attendance = [Week1, Week2, Week3, Week4]
    attendance_percentage = (sum(attendance) / 4) * 100

    # Generate attendance plot
    plt.figure(figsize=(6, 4))
    bars = plt.bar(weeks, attendance, color=["green" if x else "red" for x in attendance])
    plt.ylim(0, 1.2)
    plt.title(f"{name}'s Attendance - October")
    plt.ylabel("Attendance")
    plt.xticks(rotation=45)
    plt.yticks([0, 1], ["Absent", "Present"])
    for bar, value in zip(bars, attendance):
        plt.text(bar.get_x() + 0.1, bar.get_height() + 0.05, 'Present' if value else 'Absent', color='black')

    plt.tight_layout()
    graph_filename = "attendance_graph.png"
    plt.savefig(graph_filename)
    plt.close()

    # Email message setup
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = formataddr(("ChampionX", sender_email))
    msg['To'] = receiver_email
    msg['BCC'] = sender_email

    # Email body (HTML)
    msg.set_content("This email contains HTML content. Please enable HTML to view it.", subtype='plain')
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color:#2E86C1;">Hi {name},</h2>
        <p style="font-size: 16px;">
            You are currently at <strong>Level {level}</strong> in <strong>Toastmasters ChampionX</strong>.
        </p>
        <p style="font-size: 16px;">
            This is your <strong>Attendance Report for October</strong>. Below is your attendance summary:
        </p>
        <ul style="font-size: 16px;">
            <li><strong>Week 1:</strong> {"<span style='color:green;'>Present</span>" if Week1 else "<span style='color:red;'>Absent</span>"}</li>
            <li><strong>Week 2:</strong> {"<span style='color:green;'>Present</span>" if Week2 else "<span style='color:red;'>Absent</span>"}</li>
            <li><strong>Week 3:</strong> {"<span style='color:green;'>Present</span>" if Week3 else "<span style='color:red;'>Absent</span>"}</li>
            <li><strong>Week 4:</strong> {"<span style='color:green;'>Present</span>" if Week4 else "<span style='color:red;'>Absent</span>"}</li>
        </ul>
        <p style="font-size: 16px;">
            <strong>Your total attendance percentage:</strong> <span style="font-size: 18px; color:#117A65;"><strong>{attendance_percentage:.2f}%</strong></span>
        </p>
        <p style="font-size: 16px;">
            Here's a graphical representation of your attendance:
        </p>
        <img src="cid:attendance_graph" style="max-width:100%; border:1px solid #ccc; border-radius:10px;" alt="Attendance Graph" />
        <p style="font-size: 16px;">Thank you for being an active member of our club.</p>
        <p style="font-size: 16px;"><strong>Regards,</strong><br/>Toastmasters ChampionX Team</p>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype='html')

    # Embed image in email
    with open(graph_filename, 'rb') as img:
        img_data = img.read()
        maintype, subtype = mimetypes.guess_type(graph_filename)[0].split('/')
        msg.get_payload()[1].add_related(img_data, maintype=maintype, subtype=subtype, cid="attendance_graph")

    # Send email
    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(msg)
        print(f"Email sent to {receiver_email} with subject: {subject}")


# if __name__ == "__main__":
#     send_email(
#         subject="Invoice Due Reminder",
#         name="Akshay Kumar M",
#         receiver_email="akshay.muralibabu@gmail.com",
#         due_date="2023-10-31",
#         invoice_no="INV-21-12-009",
#         amount=1000.00
#     )