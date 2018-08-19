import smtplib
    
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # 
from email.mime.image import MIMEImage              # Изображения
import imaplib
import email
from datetime import timedelta, datetime
import time

login = 'mv150512@yandex.ru'
password = '******'

def get_datetime(msg):
    msg_date = int(msg['Date'][5:7])
    msg_month = msg['Date'][8:11]
    msg_year = int(msg['Date'][12:17])
    msg_hour = int(msg['Date'][17:19])
    msg_minutes = int(msg['Date'][20:22])
    msg_seconds = int(msg['Date'][23:25])

    month_dic = {'Jan' : 1,
                 'Feb' : 2,
                 'Mar' : 3,
                 'Apr' : 4,
                 'May' : 5,
                 'Jun' : 6,
                'Jul' : 7,
                 'Aug' : 8,
                 'Sep' : 9,
                 'Oct' : 10,
                 'Nov' : 11,
                 'Dec' : 12
                 }
    date_of_msg = datetime(msg_year, month_dic[msg_month], msg_date, msg_hour, msg_minutes, msg_seconds)
    return date_of_msg

def sender(image):
    addr_from = "mv150512@yandex.ru"                 # Адресат
    addr_to   = "burdin009@gmail.com"                   # Получатель
                                    
    msg = MIMEMultipart()                               # Создаем сообщение
    msg['From']    = addr_from                          # Адресат
    msg['To']      = addr_to                            # Получатель
    msg['Subject'] = 'Внимание!'                   # Тема сообщения

    body = "Обнаружено движение"
    msg.attach(MIMEText(body, 'plain'))                 # Добавляем в сообщение текст

    filename = image
    with open(filename, 'rb') as fp:
        file = MIMEImage(fp.read())
        fp.close()
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки msg.attach(file)
    msg.attach(file)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465) # Создаем объект SMTP
    server.login(login, password) # Получаем доступ
    server.send_message(msg) # Отправляем сообщение
    server.quit() # Выходим
    
def email_checker(status):
    while True:
        mail = imaplib.IMAP4_SSL('imap.yandex.ru')
        mail.login(login, password)
        mail.list()
        mail.select('INBOX')

        data = mail.search(None, 'ALL')
        ids = data[1]
        lates_email_id = ids[0].split()[-1]
        data = mail.fetch(lates_email_id, '(RFC822)')
        msg = email.message_from_bytes(data[1][0][1])
        msg_data = get_datetime(msg)
        
        if (msg['Subject'] == 'Get Status') and (status.get_status() == 1) and ('burdin009@gmail.com' in msg['From']): #and (msg_data >= datetime.now() - timedelta(seconds=60))
            addr_from = "mv150512@yandex.ru"                 # Адресат
            addr_to   = "burdin009@gmail.com"                   # Получатель
                                        
            msg_send = MIMEMultipart()                               # Создаем сообщение
            msg_send['From']    = addr_from                          # Адресат
            msg_send['To']      = addr_to                            # Получатель
            msg_send['Subject'] = 'On guard'                   # Тема сообщения

            body = "all right"
            msg_send.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465) # Создаем объект SMTP
            server.login(login, password) # Получаем доступ
            server.send_message(msg_send) # Отправляем сообщение
            server.quit() # Выходим
        time.sleep(60)
        
