count = int(input())
for row in range(count):
    book_ref, book_date, total_amount = input().split(',')
    rub, kop = total_amount.split('.')
    print(f'Номер бронирования {book_ref}, забронирован {book_date}. Цена: {rub} руб. {kop} коп.')    