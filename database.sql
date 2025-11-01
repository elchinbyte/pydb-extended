CREATE TABLE departament (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100)
);

CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    country_type VARCHAR(50)
);

CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    last_name VARCHAR(100),
    country_id INT REFERENCES country(id),
    departament_id INT REFERENCES departament(id),
    salary NUMERIC(10,2),
    email VARCHAR(150),
    phone VARCHAR(20)
);
