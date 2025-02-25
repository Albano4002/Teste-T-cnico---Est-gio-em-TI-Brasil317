CREATE TABLE IF NOT EXISTS noticias (
    id SERIAL PRIMARY KEY,
    titulo TEXT,
    link TEXT,
    data_extracao TIMESTAMP DEFAULT NOW()
);
