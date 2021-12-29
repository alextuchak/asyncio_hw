import asyncio
import aiosqlite
import aiosmtplib
from email.message import EmailMessage
import config
import time


async def get_contacts():
    async with aiosqlite.connect('contacts.db') as db:
        async with db.execute("SELECT * FROM contacts") as cursor:
            async for contact in cursor:
                yield contact


async def send_message(user_email, user_first_name, user_last_name):
    message = EmailMessage()
    message["From"] = "root@localhost"
    message["To"] = user_email
    message["Subject"] = 'Благодарность'
    message.set_content(f"Уважаемый, {user_first_name} {user_last_name}!\n "
                        f"Cпасибо, что пользуетесь нашим сервисом объявлений.")
    connection = aiosmtplib.SMTP(hostname=config.host_name, port=config.port)
    await connection.connect()
    await connection.login(config.login, config.password)
    await connection.send_message(message)
    time.sleep(0.45)


async def main():
    async for contact in get_contacts():
        await send_message(contact[3], contact[1], contact[2])
        print(f'Сообщение отправлено {contact[1]} {contact[2]} на email {contact[3]}')


if __name__ == '__main__':
    asyncio.run(main())
