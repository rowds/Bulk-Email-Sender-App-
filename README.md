# Bulk Email Sender App

This Python application allows you to send bulk emails with ease. It is built with tkinter for a user-friendly GUI experience.

## Features

- Send bulk emails from multiple sender accounts.
- Attach images to your emails.
- Customize the body of your emails with unique user IDs and order IDs.
- Log all sent emails and errors encountered during the process.
- User-friendly GUI built with tkinter.
- Start from where left off if the script or the app is terminated midway. (BETA feature, sometime repeats few recipients when restarts)

## How to Use

To run the Pyrhon script:
1. Clone this repository to your local machine.
2. Install the necessary Python libraries with `pip install -r requirements.txt`.
3. Delete the emails_sent.csv file, it will auto-generate when you run the code.
4. Run the script with `python main.py`.
5. Use the GUI to select your user CSV file, recipient CSV file, message directory, and optional image file.
6. Input your reply-to email address, the subject of your email, and your name.
7. Click 'Send Emails' to start sending the emails.

You can also use the standalone Emaail Sender.exe file, without installing any python enviorment. In that case follow the previously mentioned steps, start from step 3 and skip step 4. 

## CSV File Formats

- The user CSV file should contain the sender's email and password in each row.
- The recipient CSV file should contain the recipient's email in each row.

## Note

Please ensure that you have the necessary permissions to send emails from the sender accounts. Also, be aware of the sending limits of your email provider to avoid getting your account blocked.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT

