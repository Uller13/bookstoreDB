from aiohttp import web
from sqlalchemy import create_engine, MetaData, Table, func


'''Метод получения информации о пользователе'''
async def get_user(request):
    user_id = '{}'.format(request.match_info['id'])
    sql_query = 'select * from users where id = {user_id}'.format(user_id=user_id)
    result = sql_engine.execute(sql_query)
    return web.Response(text=str(result.fetchall()))


'''Метод получения истории покупок пользователя'''
async def get_purchase_history(request):
    user_id = '{}'.format(request.match_info['user'])
    sql_query = '''select 
    orders.id,
    orders.reg_date,
    orderitems.book_id,
    orderitems.book_quantity,
    orderitems.shop_id
    from orderitems
    inner join orders on orders.id = orderitems.order_id
    where orders.user_id = {user_id}'''.format(user_id=user_id)
    result = sql_engine.execute(sql_query)
    return web.Response(text=str(result.fetchall()))

'''Метод размещения заказа'''
async def post_order(request):
    book_ids = request.query['book_ids']
    book_ids = book_ids.split(',')
    book_qs = request.query['book_qs']
    book_qs = book_qs.split(',')
    user_id = request.query['user_id']
    shop_id = request.query['shop_id']
    sql_query = '''insert into orders (reg_date, user_id)           
                   values
                   (now(), {user_id})'''.format(user_id=user_id)        # Добавление заказа в БД
    sql_engine.execute(sql_query)
    order_id = get_latest_order()

    for book in book_ids:
        current_book = 0
        '''Добавление предметов заказа в БД'''
        sql_query = '''
                        insert into orderitems (order_id, book_id, book_quantity, shop_id)
                        values
                        ({order_id}, {book_id}, {book_quantity}, {shop_id});
                        '''.format(order_id=order_id, book_id=book, book_quantity=book_qs[current_book], shop_id=shop_id)
        sql_engine.execute(sql_query)
        '''Корректировка информации о состянии склада магазина (вычитание книг со склада)'''
        sql_query = '''
                        insert into stocks (shop_id, book_id, quantity)
                        values
                        ({shop_id}, {book_id}, {neg_book_quantity});
                        '''.format(shop_id=shop_id, book_id=book, neg_book_quantity=str(-int(book_qs[current_book])))
        sql_engine.execute(sql_query)
        current_book += 1

    return web.Response(status=201, text='Order successfully added')

'''Получение ассортимента магазина'''
async def get_shop_stock(request):
    final_output = []
    output = []
    shop_id = '{}'.format(request.match_info['shop'])
    total_books = calculate_total_books()
    for book in range(1, total_books + 1):
        sql_query = 'select book_id, SUM(quantity) from stocks where shop_id = {shop_id} and book_id = {book_id}'. \
            format(shop_id=shop_id, book_id=book)
        result = sql_engine.execute(sql_query)
        output.append(result.fetchall())
        final_output.append([output[book-1][0][0], int(output[book-1][0][1])]) # Грязно, но работает чтобы не выдать в
    return web.Response(text=str(final_output))                                # неверном формате

'''Вспомогательная функция рассчета полного ассортимента книг, записаных в БД'''
def calculate_total_books():
    sql_query = 'select max(id) from books'
    result = sql_engine.execute(sql_query)
    total_books = result.fetchall()[0][0]
    return total_books

'''Вспомогательная функция получения последнего заказа'''
def get_latest_order():
    sql_query = 'select max(id) from orders'
    result = sql_engine.execute(sql_query)
    latest_order = result.fetchall()[0][0]
    return latest_order


'''SQL INIT'''
PATH_TO_SQL = 'mysql+pymysql://newuser:password@localhost:3306/bookstore'
'''Формат пути = СУБД+Диалект://Имя_пользователя:пароль@адрес_сервера:порт/название_БД'''
sql_engine = create_engine(PATH_TO_SQL, pool_recycle=3600)
metadata = MetaData()
books = Table('books', metadata, autoload=True, autoload_with=sql_engine)
shops = Table('shops', metadata, autoload=True, autoload_with=sql_engine)
orders = Table('orders', metadata, autoload=True, autoload_with=sql_engine)
users = Table('users', metadata, autoload=True, autoload_with=sql_engine)
orderitems = Table('orderitems', metadata, autoload=True, autoload_with=sql_engine)
stocks = Table('stocks', metadata, autoload=True, autoload_with=sql_engine)
'''SQL INIT'''

'''AIOHTTP SERVER INIT'''
app = web.Application()
routes = [web.get('/user/{id}', get_user),
          web.get('/history/{user}', get_purchase_history),
          web.get('/stock/{shop}', get_shop_stock),
          web.post('/neworder', post_order)]
app.add_routes(routes)
web.run_app(app)
'''AIOHTTP SERVER INIT'''
