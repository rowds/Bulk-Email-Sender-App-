import smtplib, ssl, csv, random, os, time
from tkinter import filedialog, messagebox, Entry, Label, StringVar
from email.message import EmailMessage
from email.mime.image import MIMEImage
import tkinter as tk

class ErrorDialog(tk.Toplevel):
    def __init__(self, parent, text):
        tk.Toplevel.__init__(self, parent)
        self.title("Error")
        self.configure(bg='black')
        self.label = tk.Label(self, text=text, bg='black', fg='red')
        self.label.pack(padx=50, pady=50)

def select_file(label):
    filename = filedialog.askopenfilename()
    label['text'] = filename
    return filename

def select_directory(label):
    dirname = filedialog.askdirectory()
    label['text'] = dirname
    return dirname

def select_image(label):
    filename = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif')])
    label['text'] = filename
    return filename

def read_sent_emails_log():
    sent_recipients1 = set()
    try:
        with open("emails_sent.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if present
            for row in reader:
                recipient = row[1].strip().strip("[]").replace("'", "")
                sent_recipients1.add(recipient)
    except FileNotFoundError:
        pass
    return sent_recipients1

def send_emails(usercsv, mailscsv, message_dir, replyto, subject, name, image):
    counter = {}
    failed_senders = {}
    error_counter = {}
    error_messages = []
    sent_recipients = read_sent_emails_log()

    with open(usercsv) as f:
        data = [row for row in csv.reader(f)]

    # Get all message files in the selected directory
    file_list = [os.path.join(message_dir, f) for f in os.listdir(message_dir) if f.endswith('.txt')]

    with open(mailscsv, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            recipient = row[0].strip()
            if recipient in sent_recipients:
                continue             
            while True:
                random_user = random.choice(data)
                sender = random_user[0]
                password = random_user[1]

                if sender not in counter:
                    counter[sender] = 0

                if sender not in error_counter:
                    error_counter[sender] = 0

                # if sender email has already sent 400 emails or encountered error for three times, continue to the next sender instead
                if counter[sender] >= 400 or error_counter[sender] >= 3:
                    continue

                try:
                    context = ssl.create_default_context()
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
                    server.login(sender, password)
                    em = EmailMessage()
                    em['from'] = f'{name} <{sender}>'
                    if replyto:  # Only add reply-to if it's not empty
                        em['Reply-To'] = replyto
                    em['To'] = row
                    em['subject'] = subject

                    random_file = random.choice(file_list)
                    with open(random_file, 'r', encoding = 'utf-8') as file:
                        html_msg = file.read()
                    em.add_alternative(html_msg, subtype='html')

                    # Attach the image to the email if an image file has been selected
                    if image != 'No image selected':
                        try:
                            with open(image, 'rb') as img:
                                msg_image = MIMEImage(img.read())
                            msg_image.add_header('Content-ID', '<image1>')
                            em.attach(msg_image)
                        except Exception as e:
                            print(f"Error attaching image {image}:", e)
                            return f"Error attaching image {image}: {e}"

                    server.send_message(em)
                    counter[sender] += 1
                    print(counter[sender], " emails sent", "From ", sender,  "To ", row ,"File ", random_file)


                    sent_recipients.add(recipient)
                    # Write the sent email to emails_sent.csv
                    with open("emails_sent.csv", "a", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([sender, row])

                    time.sleep(2) #add 2 seconds delay before sending another email    

                    break #Breaks the while loop

                except Exception as e:
                    print(f"Error sending email From {sender} to {row}:", e )
                    error_counter[sender] += 1
                    failed_senders[sender] = str(e)
                    error_messages.append(f"Error sending email From {sender} to {row}: {e}")
                    if error_counter[sender] >= 3:
                        error_messages.append(f"Stopped sending emails from {sender} after 3 errors. Last error: {e}")
            

    # Write the failed senders to a CSV file
    with open("failed_senders.csv", "w", newline='') as file:
        writer = csv.writer(file)
        for sender, error in failed_senders.items():
            writer.writerow([sender, error])

    # Show all error messages in a single non-modal dialog
    if error_messages:
        ErrorDialog(root, "\n".join(error_messages))


root = tk.Tk()
root.title("Email Sender")
root.configure(bg='black')

label = tk.Label(root, text='Email Sender App', bg='black', fg='red')
label.pack(fill='x')

usercsv_label = tk.Label(root, text='No file selected', bg='black', fg='red', anchor='w')
usercsv_label.pack(fill='x', expand=True)
usercsv_button = tk.Button(root, text='Select user.csv', command=lambda: select_file(usercsv_label), bg='red', fg='black')
usercsv_button.pack(fill='x')

mailscsv_label = tk.Label(root, text='No file selected', bg='black', fg='red', anchor='w')
mailscsv_label.pack(fill='x', expand=True)
mailscsv_button = tk.Button(root, text='Select mails.csv', command=lambda: select_file(mailscsv_label), bg='red', fg='black')
mailscsv_button.pack(fill='x')

message_label = tk.Label(root, text='No directory selected', bg='black', fg='red', anchor='w')
message_label.pack(fill='x', expand=True)
message_button = tk.Button(root, text='Select message directory', command=lambda: select_directory(message_label), bg='red', fg='black')
message_button.pack(fill='x')

image_label = tk.Label(root, text='No image selected', bg='black', fg='red', anchor='w')
image_label.pack(fill='x', expand=True)
image_button = tk.Button(root, text='Select Image', command=lambda: select_image(image_label), bg='red', fg='black')
image_button.pack(fill='x')

replyto_entry = Entry(root)
replyto_entry.pack(fill='x')
replyto_entry.insert(0, 'Enter your reply-to email address (optional)')

subject_entry = Entry(root)
subject_entry.pack(fill='x')
subject_entry.insert(0, 'Enter the subject of your email')

name_entry = Entry(root)
name_entry.pack(fill='x')
name_entry.insert(0, 'Enter your name')

def validate_and_send_emails():
    usercsv = usercsv_label['text']
    mailscsv = mailscsv_label['text']
    message_dir = message_label['text']
    replyto = replyto_entry.get()
    subject = subject_entry.get()
    name = name_entry.get()
    image = image_label['text']

    if usercsv == 'No file selected' or mailscsv == 'No file selected' or message_dir == 'No directory selected' or subject == '' or name == '':
        messagebox.showerror("Error", "Please fill in all fields and select all files.")
    else:
        result = send_emails(usercsv, mailscsv, message_dir, replyto, subject, name, image)
    if result:
        messagebox.showerror("Error", result)
    else:    
        messagebox.showinfo("Emails Sent", "The emails have been sent successfully!")

send_button = tk.Button(root, text='Send Emails', command=validate_and_send_emails, bg='red', fg='black')
send_button.pack(fill='x')

root.mainloop()
