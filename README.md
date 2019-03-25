## CAT&kittens: Русский академический корпус и инструмент для проверки академических текстов

САТ - это корпус академических текстов, созданный на основе наиболее актуальных (написанных позднее 2010 года)
научных текстов. Большинство текстов корпуса - статьи из журналов, входящих в принятый НИУ ВШЭ перечень изданий,
публикации в которых учитываются при назначении академических надбавок. Тексты корпуса размечены при помощи пайплайна UDpipe.

В корпусе выделяются следующие домены:

| Домен         | Токены | Тексты |
|---------------|--------|--------|
| Лингвистика   | 422042 | 75     |
| Социология    | 425075 | 52     |
| Политология   | 374904 | 78     |
| Юриспруденция | 413165 | 80     |
| Психология    | 480851 | 90     |
| Экономика     | 455448 | 74     |

Общий объём корпуса составляет ок. 2.5 млн. токенов.

На основе корпуса были созданы следующие ресурсы:

* Списки академических коллокаций размерностью от двух до шести слов. Доступны как общие списки, так и списки для каждого домена. 

* Инструмент для проверки академических текстов, выделяющий следующие отклонения от академического стиля:
  - Длинные последовательности генитивов;
  - Неправильное употребление сравнительной степени;
  - Неверное употребление сочинительных групп;
  - Слова, не встречающиеся в академических текстах;
  - Смешение употребления “я” и “мы”; 
  - Неверное употребление наклонения глаголов; 
  - Слишком длинные предложения.


Разработчики:  
Преподаватели: Михаил Копотев (Хельсинкский университет), Олеся Кисселев (Университет Техаса в Сан-Антонио), Наталья Зевахина, Светлана Толдова (НИУ ВШЭ)  
Студенты: Анастасия Баранчикова, Анна Дмитриева, Александр Климов, Станислав Краснов, Мария Фёдорова (НИУ ВШЭ)
