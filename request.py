import sqlite3
from typing import Any, List, Tuple

def execute_query(sql: str, params: Tuple[Any, ...] = (), commit: bool = False) -> List[tuple]:
    with sqlite3.connect('tasks.db') as con:
        con.execute("PRAGMA foreign_keys = ON;")  # увімкнення каскадного видалення
        cur = con.cursor()
        cur.execute(sql, params)
        if commit:
            con.commit()
        return cur.fetchall()

# ---------------------------------------
# 1. Отримати всі завдання певного користувача

sql = "SELECT * FROM tasks WHERE user_id = ?"
result = execute_query(sql, (3,))
print("1. Отримати всі завдання певного користувача:", result)

# ---------------------------------------
# 2. Отримати завдання за певним статусом

sql = """
SELECT *
FROM tasks as t
INNER JOIN status s ON t.status_id = s.id
WHERE s.name = ?;
"""
result = execute_query(sql, ("new",))
print("2. Отримати завдання за певним статусом:", result)

# ---------------------------------------
# 3. Оновити статус конкретного завдання
sql = """
UPDATE tasks 
SET status_id = ? 
WHERE id = ?
   """

result = execute_query(sql, (2,1,), True)
print("3. Оновити статус конкретного завдання")

# ---------------------------------------
# 4. Отримати список користувачів, які не мають жодного завдання
sql = """
SELECT *
FROM users
WHERE id NOT IN (SELECT user_id FROM tasks)
"""
result = execute_query(sql)
print("4. Отримати список користувачів, які не мають жодного завдання:", result)

# ---------------------------------------
# 5. Додати нове завдання для конкретного користувача
sql = """
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (?, ?, ?, ?)
"""
execute_query(sql, ("Нове завдання", "Опис нового завдання", 1, 3), commit=True)
print("5. Додано нове завдання")

# ---------------------------------------
# 6. Отримати всі завдання, які ще не завершено
sql = """
SELECT t.*
FROM tasks t
JOIN status s ON t.status_id = s.id
WHERE s.name != ?
"""
result = execute_query(sql, ("completed",))
print("6. Завдання, що не завершено:", result)

# ---------------------------------------
# 7. Видалити конкретне завдання
sql = "DELETE FROM tasks WHERE id = ?"
execute_query(sql, (1,), commit=True)
print("7. Завдання видалено")

# ---------------------------------------
# 8. Знайти користувачів з певною електронною поштою
sql = "SELECT * FROM users WHERE email LIKE ?"
result = execute_query(sql, ("%example.com%",))
print("8. Користувачі з певною електронною поштою:", result)

# ---------------------------------------
# 9. Оновити ім'я користувача
sql = "UPDATE users SET fullname = ? WHERE id = ?"
execute_query(sql, ("Нове Ім'я", 3), commit=True)
print("9. Ім'я користувача оновлено")

# ---------------------------------------
# 10. Отримати кількість завдань для кожного статусу
sql = """
SELECT s.name, COUNT(t.id) as task_count
FROM status s
LEFT JOIN tasks t ON t.status_id = s.id
GROUP BY s.name
"""
result = execute_query(sql)
print("10. Кількість завдань за статусами:", result)

# ---------------------------------------
#11. Отримати завдання, призначені користувачам з певним доменом email
sql = """
SELECT t.*
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE ?
"""
result = execute_query(sql, ("%@example.com%",))
print("11. Завдання для користувачів з певним доменом:", result)

# ---------------------------------------
# 12. Отримати список завдань, що не мають опису
sql = "SELECT * FROM tasks WHERE description IS NULL OR description = ''"
result = execute_query(sql)
print("12. Завдання без опису:", result)

# ---------------------------------------
# 13. Вибрати користувачів та їхні завдання, які у статусі 'in progress'
sql = """
SELECT u.fullname, t.title, s.name
FROM tasks t
INNER JOIN users u ON t.user_id = u.id
INNER JOIN status s ON t.status_id = s.id
WHERE s.name = ?
"""
result = execute_query(sql, ("in progress",))
print("13. Користувачі та їхні завдання у статусі 'in progress':", result)

# ---------------------------------------
# 14. Отримати користувачів та кількість їхніх завдань
sql = """
SELECT u.fullname, COUNT(t.id) as task_count
FROM users u
LEFT JOIN tasks t ON t.user_id = u.id
GROUP BY u.id
"""
result = execute_query(sql)
print("14. Користувачі та кількість їхніх завдань:", result)