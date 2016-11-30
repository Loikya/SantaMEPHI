# coding=UTF-8
import random
import mysql.connector
from config import sql_user, sql_pass, sql_host, sql_base
from string import split, lower


def register_user(vk_id, payload, gbot):
    conn = mysql.connector.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_base)
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=%s', (vk_id,))
    user = cur.fetchall()
    if (len(user) != 0):
        gbot.messages.send(peer_id=vk_id, message='Вы уже были зарегистрированы ранее!', random_id=random.randint(0, 200000))
        return
    cur.execute('INSERT INTO users (id) VALUES(%s)', (vk_id,))
    conn.commit()
    
    gbot.messages.send(peer_id=vk_id, message='Вы успешно зарегистрированы!',random_id=random.randint(0, 200000))


def delete_user(vk_id, payload, gbot):
    conn = mysql.connector.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_base)
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=%s', (vk_id,))
    user = cur.fetchall()
    if (len(user) == 0):
        gbot.messages.send(peer_id=vk_id, message='Вашего id нет в системе!',
                           random_id=random.randint(0, 200000))
        return
    cur.execute("DELETE FROM users WHERE id=%s", (vk_id,))
    conn.commit()
    gbot.messages.send(peer_id=vk_id, message='Ваш id был удален из базы', random_id=random.randint(0, 200000))


command_str_list = '\n!зарегистрироваться\n!отказаться\n!инфо\n!группа <группа>'


def show_info(vk_id, payload, gbot):
    conn = mysql.connector.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_base)
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=%s', (vk_id,))
    user = cur.fetchall()
    if (len(user) != 0):
        gbot.messages.send(peer_id=vk_id, message='Вы участвуете в игре'+command_str_list, random_id=random.randint(0, 200000))
    else:
        gbot.messages.send(peer_id=vk_id, message='Вы не участвуете в игре'+command_str_list, random_id=random.randint(0, 200000))


def set_group(vk_id, payload, gbot):
    conn = mysql.connector.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_base)
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE id=%s', (vk_id,))
    user = cur.fetchall()
    if (len(user) == 0):
        gbot.messages.send(peer_id=vk_id, message='Вы не участвуете в игре', random_id=random.randint(0, 200000))
        return
    cur.execute("UPDATE `users` SET `group`=%s WHERE `id`=%s", (payload if payload else u'нет информации', vk_id,))
    conn.commit()
    gbot.messages.send(peer_id=vk_id, message='Информация о группе была обновлена', random_id=random.randint(0, 200000))



def no_action(vk_id, payload, gbot):
    a=0


def parse_message(msg):
    msg = lower(msg)
    if msg[0] == '!':
        return split(msg[1:], None, 1)
    elif msg[0] == '/':
        return [u'self_message', '']
    else:
        return [u'***', '']


commands = ((u'зарегистрироваться',register_user),
            (u'отказаться',delete_user),
            (u'инфо',show_info),
            (u'self_message',no_action),
            (u'группа',set_group),)


def run_msg(mesg, gbot):
    if (mesg[0] != 4):
        return
    res = parse_message(mesg[6])
    for command in commands:
        if (res[0] == command[0]):
            try:
                command[1](mesg[3], res[1] if len(res)>1 else None, gbot)
                return

            except Exception as error:
                err_m = u'Что то пошло не так. Попробуйте повторить запрос или свяжитесь с администратором'
                gbot.messages.send(peer_id=mesg[3], message=err_m, random_id=random.randint(0, 200000))
                print(error)
    info_message = 'Для вывода информации введите "!инфо"'
    gbot.messages.send(peer_id=mesg[3], message=info_message, random_id=random.randint(0, 200000))
