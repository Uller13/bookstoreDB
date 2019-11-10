insert into books (name, author, isbn) 
values 
('Ego is the enemy', 'Ryan Holiday', '978-1-59184-781-6'),
('The Martian Chronicles', 'Ray Bradbury', '978-0-00-647923-9'),
('Trainspotting', 'Irvine Welsh', '978-0-099-46589-8');

insert into shops (name, address, post_code)
values
('Bookstore one', 'Book street, 13', '100100'),
('Bookstore two', 'Book lane, 11', '100110'),
('Bookstore three', 'Book boulevard, 22', '100111');

insert into users (name, surname, fathers_name, email)
values
('Vasily', 'Pupkin', 'Vasilievich', 'VPupkin@yandex.ru'),
('John', 'Doe', NULL, 'JDoe@gmail.com'),
('Mary', 'Sue', NULL, 'MSue@icloud.com');

insert into stocks (shop_id, book_id, quantity)
values
(1, 1, 0),
(1, 2, 10),
(1, 3, 10),
(2, 1, 10),
(2, 2, 0),
(2, 3, 10),
(3, 1, 10),
(3, 2, 10),
(3, 3, 0);

insert into orders (reg_date, user_id)
values
(now(), 1),
(now(), 2),
(now(), 3),
(now(), 1),
(now(), 2);

insert into orderitems (order_id, book_id, book_quantity, shop_id)
values
(1, 2, 2, 1),
(2, 2, 1, 3),
(3, 3, 1, 2),
(4, 1, 1, 3),
(5, 2, 2, 1),
(5, 3, 1, 1);