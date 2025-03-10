CREATE SCHEMA pdf_schema;

CREATE TABLE pdf_schema.pdf_files (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    editorial TEXT NOT NULL,
    cover_page INT NOT NULL DEFAULT 1 CHECK (cover_page >= 1),
    data BYTEA NOT NULL,
    favorite BOOLEAN NOT NULL DEFAULT false,
    thumbnail_image BYTEA DEFAULT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
