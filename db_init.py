import psycopg2

con = psycopg2.connect(
    dbname='remova_store',
    user='postgres',
    password='$ur psw',
    host='localhost',
    port='5432'
)

cur = con.cursor()

if __name__ == '__main__':
    cur.execute(
        f'''create table users
            (
                id           serial primary key,
                first_name   varchar(50)        not null,
                last_name    varchar(50)        not null,
                email        varchar(50) unique not null,
                phone_num    varchar(50) unique not null,
                password     varchar(50)        not null,
                admin_status bool default false
            );
            
            create table products
            (
                title       varchar(255)     NOT NULL,
                description text             NOT NULL,
                gender      varchar(10),
                category    varchar          NOT NULL,
                cost        double precision NOT NULL,
                image_url   text,
                id          serial           NOT NULL UNIQUE,
                PRIMARY KEY (id)
            );
            
            create table orders
            (
                create_date date default (now()),
                summa       double precision NOT NULL,
                user_id     integer          NOT NULL,
                id          serial           NOT NULL UNIQUE,
                PRIMARY KEY (id),
                CONSTRAINT fk_user
                    FOREIGN KEY (user_id)
                        REFERENCES users (id)
                        ON DELETE CASCADE
            );
            
            create table purchases
            (
                product_id integer NOT NULL,
                order_id   integer NOT NULL,
                CONSTRAINT fk_product
                    FOREIGN KEY (product_id)
                        REFERENCES products (id)
                        ON DELETE SET NULL,
                CONSTRAINT fk_orders
                    FOREIGN KEY (order_id)
                        REFERENCES orders (id)
                        ON DELETE CASCADE
            );
            
            create table favorites
            (
                user_id    integer NOT NULL,
                product_id integer NOT NULL,
                CONSTRAINT fk_user
                    FOREIGN KEY (user_id)
                        REFERENCES users (id)
                        ON DELETE CASCADE,
                CONSTRAINT fk_product
                    FOREIGN KEY (product_id)
                        REFERENCES products (id)
                        ON DELETE CASCADE
            );
            
            create table cart
            (
                user_id    integer NOT NULL,
                product_id integer NOT NULL,
                CONSTRAINT fk_user
                    FOREIGN KEY (user_id)
                        REFERENCES users (id)
                        ON DELETE CASCADE,
                CONSTRAINT fk_product
                    FOREIGN KEY (product_id)
                        REFERENCES products (id)
                        ON DELETE CASCADE
            );'''
    )
    con.commit()
