import csv
import psycopg2
from os import path
from config import host, user, password, db_name


connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
sql = connection.cursor()
connection.autocommit = True

def user_input():
    path = str
    print("Вы будете работать со своим csv или с transactions.csv?")
    print("1. Со своим")
    print("2. С transactions.csv")
    a = input()
    if(a == "1"):
        print("Введите путь csv")
        path = input()
    elif(a == "2"):
        path = "C:\\Users\\donat\\Downloads\\Telegram Desktop\\Цсвешки\\transactions_cut.csv"
    else:
        print("Ошибка. Неверное значение")

    return path


def csvreader(path):
    with open(path, encoding ="UTF-8") as file:
        reader = csv.reader(file)
        values = list(reader)
        #print(*values, sep="\n")
        return values


class data_base:
    def table_create(path, values, sql, connection):
        table_name = path.split("\\")[-1]
        print(table_name)
        table_elements = csvreader(path)[0]
        print(table_elements)
        sql.execute(f"CREATE TABLE IF NOT EXISTS transactions " +
                    f"(customer_id integer, tr_datetime varchar(255),"
                    f"mcc_code varchar(255), tr_type varchar(255), amount FLOAT, term_id text)")
        connection.commit()
        return table_name, table_elements
    def table_fill(path, values, sql, connection):
        table_name = path.split("\\")[-1]
        table_lines = csvreader(path)
        table_elements = csvreader(path)[0]
        for i in table_lines:
            if i[0] != "customer_id":
               sql.execute(f"INSERT INTO "+
                           f"transactions (customer_id, tr_datetime,mcc_code , tr_type, amount, term_id)"
                           f"values({int(i[0])},'{i[1]}','{i[2]}' , '{i[3]}',{float(i[4])}, '{i[5]}')")


    def calculate_median_value(path, sql, connection):
        median_value = 0
        print("Как вы хотите посчитать медианное значение?")
        print("1.Обычный поиск по всем значениям (стандартное поведение)")
        print("2.Поиск по тем строкам, которые ни в одном из своих столбцов не содержат пустые значения")
        print("3.Медиана суммы транзакций по строкам, отсортированным по полю amount в порядке возрастания, и из которых удалены дублирующиеся по столбцам [mcc_code, tr_type] строки, причём при удалении соответстующих дублей остаются")
        a = input()
        if a == "1":
            sql.execute(f"""SELECT AVG(amount)
               FROM (SELECT amount
               FROM transactions
               ORDER BY amount
               LIMIT 2
               OFFSET (SELECT (COUNT(*) - 1) / 2
               FROM transactions)) AS FOO""")
            median_value = sql.fetchone()
        elif a == "2":
            sql.execute("""SELECT AVG(amount)
                 FROM (SELECT customer_id, amount, term_id, mcc_code, tr_type
                 FROM transactions
                 WHERE term_id != ''
                 ORDER BY amount
                 LIMIT 2
                 OFFSET (SELECT (COUNT(*) - 1) / 2
                 FROM transactions)) AS FOO""")
            median_value = sql.fetchone()
        elif a == "3":
            sql.execute()
            median_value = sql.fetchone()
        else:
            print("Ошибка. Неверное значение")
        print("Выберите куда вывести медианно значение :")
        print("1. В csv файл")
        print("2. На экран")
        a = input()
        if a == "1":
            with open(r"C:\Users\donat\Downloads\Telegram Desktop\Цсвешки\Лист Microsoft Excel.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["median value"])
                writer.writerow(median_value)
        elif a == "2":
            print(median_value)
        else:
            print("Ошибка. Неверное значение")
        return median_value





def main():
    try:
    except Exception as e:
        print("Ошибка подключения к Базе данных", e)
    finally:
        path = user_input()
        values = csvreader(path)
        data_base.table_create(path, sql, connection)
        data_base.table_fill(path, sql, connection)
        data_base.calculate_median_value(path, sql, connection)







if __name__ == "__main__":
    main()






