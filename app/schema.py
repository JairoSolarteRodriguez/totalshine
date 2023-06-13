instructions = [
    'DROP TABLE IF EXISTS user_app CASCADE;',
    'DROP TABLE IF EXISTS role CASCADE;',
    'DROP TABLE IF EXISTS review CASCADE;',
    'DROP TABLE IF EXISTS review_user CASCADE;',
    'DROP TABLE IF EXISTS schedule CASCADE;',
    'DROP TABLE IF EXISTS contact CASCADE;',
    'DROP TABLE IF EXISTS product CASCADE;',
    'DROP TABLE IF EXISTS hire CASCADE;',
    'DROP TABLE IF EXISTS image CASCADE;',
    """
        CREATE TABLE user_app(
            id_user SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone_number VARCHAR(50),
            password TEXT NOT NULL
        );
    """,
    """
        CREATE TABLE role(
            id_role SERIAL PRIMARY KEY,
            id_user INT NOT NULL, 
            rol VARCHAR(25) NOT NULL,

            FOREIGN KEY (id_user) REFERENCES user_app (id_user)
        );

    """,
    """
        CREATE TABLE review(
            id_review SERIAL PRIMARY KEY,
            comment TEXT,
            stars INT NOT NULL
        );
    """,
    """
        CREATE TABLE review_user(
            id_review_user SERIAL PRIMARY KEY,
            id_user INT NOT NULL,
            id_review INT NOT NULL,

            FOREIGN KEY (id_user) REFERENCES user_app (id_user),
            FOREIGN KEY (id_review) REFERENCES review (id_review)
        );
    """,
    """
        CREATE TABLE schedule(
            id_schedule SERIAL PRIMARY KEY,
            id_user INT NOT NULL,
            scheduling_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            schedule_for TIMESTAMP NOT NULL,
            address VARCHAR(150),
            phone VARCHAR(50),
            notes TEXT,
            schedule_state VARCHAR(20) NOT NULL DEFAULT 'scheduled',
            email VARCHAR(255) NOT NULL,

            FOREIGN KEY (id_user) REFERENCES user_app (id_user)
        );
    """,
    """
        CREATE TABLE image(
            id_image SERIAL PRIMARY KEY,
            image_url TEXT NOT NULL,
            created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            type VARCHAR(50) DEFAULT 'gallery'
        );
    """,
    """
        CREATE TABLE review_image(
            id_review_image SERIAL PRIMARY KEY,
            id_review INT NOT NULL,
            id_image INT NOT NULL,

            FOREIGN KEY (id_review) REFERENCES review (id_review),
            FOREIGN KEY (id_image) REFERENCES image (id_image)
        );
    """,
    """
        CREATE TABLE hire(
            id_hire SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            url_image TEXT
        );
    """,
    """
        CREATE TABLE product(
            id_product SERIAL PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            description TEXT,
            url_image TEXT,
            price VARCHAR(100),
            active BOOLEAN DEFAULT true
        );
    """,
    """
        CREATE TABLE contact(
            id_contact SERIAL PRIMARY KEY,
            name VARCHAR(150),
            email VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            phone VARCHAR(50)
        );
    """
]