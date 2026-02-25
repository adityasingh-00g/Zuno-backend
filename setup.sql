CREATE DATABASE rag_chat;

CREATE USER rag_user WITH PASSWORD 'strongpassword';

GRANT ALL PRIVILEGES ON DATABASE rag_chat TO rag_user;
