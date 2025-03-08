CREATE SCHEMA pdf_schema;

CREATE TABLE pdf_schema.pdf_files (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    data BYTEA NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
