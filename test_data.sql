CREATE TABLE IF NOT EXISTS refs (
    id SERIAL PRIMARY KEY,
    entry_type TEXT NOT NULL,
    citation_key TEXT UNIQUE NOT NULL,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    tag TEXT,
    extra_fields JSON NOT NULL
);
