import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from typing import List
from models import Task
import os
import pendulum

load_dotenv()


class EmailNotifier:
    smtp_server: str
    smtp_port: int
    sender: str
    password: str
    recipients: str | List[str]
    tasklist: List[Task]

    def __init__(self, recipients: str | List[str], tasklist: List[Task]):
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        sender = os.getenv("SENDER")
        password = os.getenv("PASSWORD")

        if smtp_server is None:
            raise EnvironmentError("Environment variable SMTP_SERVER is not set.")
        if smtp_port is None:
            raise EnvironmentError("Environment variable SMTP_PORT is not set.")
        if sender is None:
            raise EnvironmentError("Environment variable SENDER is not set.")
        if password is None:
            raise EnvironmentError("Environment variable PASSWORD is not set.")

        self.recipients = recipients
        self.tasklist = sorted(tasklist, key=lambda task: task.deadline)

    def _generate_html(self) -> str:
        html = """
        <html>
        <body>
            <h2>Task List</h2>
            <table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                <th>Task Name</th>
                <th>Description</th>
                <th>Deadline</th>
                </tr>
            </thead>
            <tbody>
        """

        for task in self.tasklist:
            html += f"""
                <tr>
                <td>{task.task_name}</td>
                <td>{task.task_description}</td>
                <td>{task.deadline.to_day_datetime_string()}</td>
                </tr>
            """

        html += """
            </tbody>
            </table>
        </body>
        </html>
        """
        return html

    def send_email(self):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = (
            f"Task Reminder - {pendulum.now('local').to_formatted_date_string()}"
        )
        msg["From"] = self.sender
        msg["To"] = ", ".join(self.recipients)

        html_content = self._generate_html()

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender, self.password)
            server.send_message(msg, from_addr=self.sender, to_addrs=self.recipients)

        print("Secure HTML email sent!")


if __name__ == "__main__":
    notifier = EmailNotifier(
        "test",
        [
            Task(
                "test1",
                "desc1",
                pendulum.DateTime(2025, 12, 12, 0, 0, tzinfo=pendulum.local_timezone()),
            ),
            Task(
                "test2",
                "desc2",
                pendulum.DateTime(2025, 11, 12, 0, 0, tzinfo=pendulum.local_timezone()),
            ),
            Task(
                "test3",
                "desc3",
                pendulum.DateTime(2025, 12, 31, 0, 0, tzinfo=pendulum.local_timezone()),
            ),
        ],
    )

    html = notifier._generate_html()

    print(html)
