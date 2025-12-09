-- Create User Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL -- 'Client' or 'Support'
);

-- Create Queries Table
CREATE TABLE queries (
    query_id SERIAL PRIMARY KEY,
    client_email VARCHAR(100),
    client_mobile VARCHAR(15),
    query_heading VARCHAR(255),
    query_description TEXT,
    status VARCHAR(20) DEFAULT 'Open',
    date_raised TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_closed TIMESTAMP NULL 
);
