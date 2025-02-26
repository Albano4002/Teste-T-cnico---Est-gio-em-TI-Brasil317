CREATE TABLE noticias (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    link TEXT NOT NULL,
    data_extracao TIMESTAMP NOT NULL DEFAULT NOW()
);
