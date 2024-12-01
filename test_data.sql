CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL,
    title TEXT NOT NULL,
    publisher TEXT NOT NULL,
    address TEXT,
    volume TEXT,
    series TEXT,
    edition TEXT,
    month TEXT,
    note TEXT,
    url TEXT
);

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

INSERT INTO refs (entry_type, citation_key, author, title, year, tag, bibtex) VALUES (
    'book', 
    'box_2015_time', 
    'Box, George EP and Jenkins, Gwilym M and Reinsel, Gregory C and Ljung, Greta M', 
    'Time series analysis: forecasting and control', 
    '2015', 
    '-', 
    '@book{box_2015_time,
    title={Time series analysis: forecasting and control},
    author={Box, George EP and Jenkins, Gwilym M and Reinsel, Gregory C and Ljung, Greta M},
    year={2015},
    publisher={John Wiley \& Sons}
}');

INSERT INTO refs (entry_type, citation_key, author, title, year, tag, bibtex) VALUES (
    'book', 
    'huyen_2022_designing',
    'Huyen, Chip',
    'Designing machine learning systems',
    '2022', 
    '-',
    '@book{huyen_2022_designing,
    title={Designing machine learning systems},
    author={Huyen, Chip},
    year={2022},
    publisher={OReilly Media, Inc.}
}');
