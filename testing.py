median_value = 0
      print("Как вы хотите посчитать медианное значение?")
      print("1.Обычный поиск по всем значениям (стандартное поведение)")
      print("2.Поиск по тем строкам, которые ни в одном из своих столбцов не содержат пустые значения")
      print("3.Медиана суммы транзакций по строкам, отсортированным по полю amount в порядке возрастания, и из которых удалены дублирующиеся по столбцам [mcc_code, tr_type] строки, причём при удалении соответстующих дублей остаются только последние из дублирующихся строк")
      a = input()
      if a == 1:
       sql.execute(f"""SELECT AVG(amount)
               FROM (SELECT amount
               FROM transactions
               ORDER BY amount
               LIMIT 2
               OFFSET (SELECT (COUNT(*) - 1) / 2
               FROM transactions)) AS FOO""")
       median_value = sql.fetchone()
      elif a == 2:
        sql.execute("""SELECT AVG(amount)
        FROM (SELECT customer_id, amount, term_id, mcc_code, tr_type
        FROM transactions
        WHERE term_id != ''
        ORDER BY amount
        LIMIT 2
        OFFSET (SELECT (COUNT(*) - 1) / 2
        FROM transactions)) AS FOO""")
        median_value = sql.fetchone()
      return median_value