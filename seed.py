from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_USERS = 10
NUMBER_TASKS = 20

def generate_fake_data(number_users, number_tasks) -> tuple():
    fake_users = []# тут зберігатимемо користувачів
    fake_tasks = []# тут зберігатимемо таски
    statuses = [(s,) for s in ['new', 'in progress', 'completed']] # статуси сталі значення

    fake_data = faker.Faker()

# Створимо набір юзерів у кількості NUMBER_USERS
    for _ in range(number_users):
        email = fake_data.unique.email()
        fullname = fake_data.name()
        fake_users.append((email, fullname))

 # Створимо набір тасок  у кількості NUMBER_TASKS
    for _ in range(number_tasks):
        title = fake_data.sentence(nb_words=5)  # коротка назва задачі
        description = fake_data.text(max_nb_chars=100)  # опис задачі
        user_id = randint(1, number_users)  # випадковий користувач
        status_id = randint(1, len(statuses))  # випадковий статус (1,2,3)
        fake_tasks.append((title, description, user_id, status_id))

    return fake_users, fake_tasks, statuses

def insert_data_to_db(users, status_list, tasks):
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        # Вставка даних
        cur.executemany("INSERT INTO users (email, fullname) VALUES (?, ?)", users)
        cur.executemany("INSERT OR IGNORE INTO status (name) VALUES (?)", status_list)
        cur.executemany("INSERT INTO tasks (title, description, user_id, status_id) VALUES (?, ?, ?, ?)", tasks)

        con.commit()
    print(f"{len(users)} users, {len(status_list)} statuses, {len(tasks)} tasks added to DB.")

if __name__ == "__main__":
    users, tasks, statuses = generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    insert_data_to_db(users, statuses, tasks)