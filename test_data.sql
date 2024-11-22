CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL,
    author VARCHAR(100) TEXT NOT NULL,
    year VARCHAR(4) NOT NULL,
    title TEXT NOT NULL,
    publisher TEXT NOT NULL,
    address TEXT,
    volume VARCHAR(50),
    series TEXT,
    edition VARCHAR(50),
    month VARCHAR(20),
    note TEXT,
    url TEXT
);

CREATE TABLE IF NOT EXISTS refs (
    id SERIAL PRIMARY KEY,
    entry_type VARCHAR(50) NOT NULL,
    citation_key VARCHAR(100) UNIQUE NOT NULL,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year VARCHAR(4) NOT NULL,
    tag VARCHAR(50),
    bibtex TEXT NOT NULL
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