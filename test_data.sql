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
    'box2015time', 
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
    'huyen2022designing',
    'Huyen, Chip',
    'Designing machine learning systems',
    '2022', 
    '-',
    '@book{huyen_2022_designing,
    title={Designing machine learning systems},
    author={Huyen, Chip},
    year={2022},
    publisher={O''Reilly Media, Inc}
}');

INSERT INTO refs (entry_type, citation_key, author, title, year, tag, bibtex) VALUES (
    'book', 
    'virtanen2021tekoaly', 
    'Virtanen, Matti and Korhonen, Anna', 
    'Tekoäly ja koneoppiminen Suomessa', 
    '2021', 
    '-', 
    '@book{virtanen2021tekoaly,
        title={Tekoäly ja koneoppiminen Suomessa},
        author={Virtanen, Matti and Korhonen, Anna},
        year={2021},
        publisher={Tietokustannus},
        address={Helsinki, Suomi},
        volume={3},
        series={Tietotekniikan kehitys},
        edition={1st},
        month={June},
        note={Analyysi tekoälyn vaikutuksista suomalaisessa yhteiskunnassa},
        url={https://esimerkki.fi/tekoaly-ja-koneoppiminen}
    }'
);