import vk
import requests
import time
import random
import sqlite3

def group_auth_vk(token):
    session = vk.Session(access_token=token)
    return vk.API(session, v='5.60')

def user_auth_vk(id, login, passwd, scope):
    session = vk.AuthSession(app_id=id, user_login=login, user_password=passwd, scope=scope)
    return vk.API(session, v='5.60')

def register_user(vk_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=?',(vk_id,))
    user = cur.fetchall()
    if (len(user) != 0):
        gbot.messages.send(peer_id=vk_id, message='Вы уже были зарегестрированы ранее!', random_id=random.randint(0, 200000))
        return
    user = ubot.users.get(user_ids=vk_id)[0]
    firstName = user['first_name']
    secondName = user['last_name']
    cur.execute('INSERT INTO users (id, firstName, secondName) VALUES(?, ?, ?)', (vk_id, firstName, secondName))
    conn.commit()
    gbot.messages.send(peer_id=vk_id, message='Вы успешно зарегестрированы!\n Для указания дополнительной информации о себе используйте /доп_информация',random_id=random.randint(0, 200000))

def delete_user(vk_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=?', (vk_id,))
    user = cur.fetchall()
    if (len(user) == 0):
        gbot.messages.send(peer_id=vk_id, message='Вашего id нет в системе!',
                           random_id=random.randint(0, 200000))
        return
    cur.execute("DELETE FROM users WHERE id=?", (vk_id,))
    conn.commit()
    gbot.messages.send(peer_id=vk_id, message='Ваш id был удален из базы', random_id=random.randint(0, 200000))

def set_about(vk_id, text):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=?', (vk_id,))
    user = cur.fetchall()
    if (len(user) == 0):
        gbot.messages.send(peer_id=vk_id, message='Вашего id нет в системе!',
                           random_id=random.randint(0, 200000))
        return
    cur.execute('UPDATE users SET about=? WHERE id=?', (text, vk_id,))
    conn.commit()
    gbot.messages.send(peer_id=vk_id, message='Дополнительная информация о вас обновлена. Новая информация: .\n'+text, random_id=random.randint(0, 200000))


def main():
    global gbot
    global ubot
    token = 'ebebc4075af9afeb6a90a86b0190d114502bdc447de7bc59cf9b6ed17c5f481086b3796f1531d45f08a2a'
    gbot = group_auth_vk(token)
    ubot = user_auth_vk('5419077', "8****", "*******", 'wall,messages,photos,audio') # (id приложения, номер телефона, пароль, права доступа)

    info_message = 'Здравствуйте! \nДля регистрации напишите "/зарегестрироваться"\n Для отказа от участия напишите "/отказаться"'


    print("Ready!")
    while (True):
        try:
            poll = gbot.messages.getLongPollServer()
            r = requests.request("GET", "http://" + poll['server'] + "?act=a_check&key=" + poll['key'] + "&ts=" + str(
                poll['ts']) + "&wait=25&mode=2", timeout=50)
            mesg_poll = r.json()
            msg = gbot.messages.getById(message_ids=118)
        except Exception:
            print("Error")
            time.sleep(4)
            poll = gbot.messages.getLongPollServer()
            continue
        finally:
            for mesg in mesg_poll['updates']:
                if (mesg[0] != 4):
                    continue
                if (mesg[6] == '/доп_информация'):
                    continue
                if (mesg[6] == '/зарегестрироваться'):
                    try:
                        register_user(mesg[3])
                        continue

                    except Exception as error:
                        gbot.messages.send(peer_id=mesg[3],
                                          message='Что то пошло не так. Попробуйте повторить запрос или свяжитесь с администратором',
                                          random_id=random.randint(0, 200000))
                        print(error)
                        continue

                if (mesg[6] == '/отказаться'):
                    try:
                        delete_user(mesg[3])
                        continue

                    except Exception as error:
                        gbot.messages.send(peer_id=mesg[3],
                                          message='Что то пошло не так. Попробуйте повторить запрос или свяжитесь с администратором',
                                          random_id=random.randint(0, 200000))
                        print(error)
                        continue

                last_mesg = gbot.messages.getById(message_ids=mesg[1]-1)["items"][0]["body"] #GOVNOKOD DETECTED!
                if(last_mesg == "/доп_информация"):
                    try:
                        set_about(mesg[3], mesg[6])
                        continue

                    except Exception as error:
                        gbot.messages.send(peer_id=mesg[3],
                                          message='Что то пошло не так. Попробуйте повторить запрос или свяжитесь с администратором',
                                          random_id=random.randint(0, 200000))
                        print(error)
                        continue

                gbot.messages.send(peer_id=mesg[3], message=info_message, random_id=random.randint(0, 200000))



if __name__ == '__main__':
    main()