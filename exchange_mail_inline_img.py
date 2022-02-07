
from exchangelib import Credentials, Account, Message, Mailbox, FileAttachment, Configuration, DELEGATE, HTMLBody
if __name__ == "__main__":
    user = ''
    passwd = ''

    credentials = Credentials(user, passwd)
    config = Configuration(server='outlook.office365.com', credentials=credentials)
    account = Account(primary_smtp_address=user,credentials=credentials,config=config)

    # for item in account.inbox.all().order_by('-datetime_received')[:10]:
    #     print(item.subject, item.sender, item.datetime_received)

    message = Message(account=account)
    att_filename = "C:\\Users\\test\\test.png"
    with open(att_filename, 'rb') as f:
        my_logo = FileAttachment(
            name=att_filename, content=f.read(),
            is_inline=True, content_id=att_filename,
        )
    message.attach(my_logo)
    to_recipients=[]

    to_recipients.append(Mailbox(email_address='test@test.co.kr'))
    to_recipients.append(Mailbox(email_address='test2@test.com'))
    message.subject = 'test-mail'
    message.to_recipients = to_recipients
    message.body = HTMLBody(
        '<html><body>Hello logo: <img src="cid:%s"></body></html>' %att_filename
        )
    print(att_filename)
    # message.send()
