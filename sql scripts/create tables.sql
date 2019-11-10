CREATE TABLE IF NOT EXISTS Users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    surname VARCHAR(100),
    fathers_name VARCHAR(100),
    email VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Books (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    author VARCHAR(100),
    isbn VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Shops(
	id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    address VARCHAR(100),
    post_code VARCHAR(100),
    PRIMARY KEY (id)
    );
    
    
CREATE TABLE IF NOT EXISTS Orders(
	id INT NOT NULL AUTO_INCREMENT,
    reg_date DATETIME,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    PRIMARY KEY (id)
    );

CREATE TABLE IF NOT EXISTS OrderItems(
	id INT NOT NULL AUTO_INCREMENT,
    order_id INT,
    book_id INT,
    book_quantity INT,
    shop_id INT,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (book_id) REFERENCES Books(id),
    FOREIGN KEY (shop_id) REFERENCES Shops(id),
    PRIMARY KEY (id)
    );
    
CREATE TABLE IF NOT EXISTS Stocks(
	id INT NOT NULL AUTO_INCREMENT,
    shop_id INT,
    book_id INT,
    quantity INT,
    FOREIGN KEY (shop_id) REFERENCES Shops(id),
    FOREIGN KEY (book_id) REFERENCES Books(id),
    PRIMARY KEY (id)
    );