# URL-Shortener
## 1) Query used to create url_shortener table
```
create table url_shortener(
	id serial primary key,
	original_url text,
	short_url varchar(6) unique,
	created_at timestamptz default now()
);
```
## 2) Inserting sample data
```
insert into url_shortener(original_url, short_url)
	values	('https://example-01.com', '1'),
            ('https://example-02.com', '2');
```
![Table with sample data](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Table%20data.png)
## 3) Inserting 1000 rows
Inserting original url's first</br>

__Query__
```
INSERT INTO url_shortener (original_url) VALUES %s RETURNING id;
```
__Eg.__ 
```
INSERT INTO url_shortener (original_url) VALUES
    ('https://www.some-website.com/page/item_0'),
    ('https://www.some-website.com/page/item_1'),
    ('https://www.some-website.com/page/item_2'),
    -- ... up to 10,000 rows per batch ...
    ('https://www.some-website.com/page/item_9999')
RETURNING id;
```
Updating the inserted URL's short code</br>

__Query__
```
UPDATE url_shortener SET short_url = data.short_url
        FROM (VALUES %s) AS data (id, short_url)
        WHERE url_shortener.id = data.id;
```
__Eg.__
```
UPDATE url_shortener
SET short_url = data.short_url
FROM (VALUES
    (12345, 'abc123'),
    (12346, 'abc124'),
    (12347, 'abc125')
    -- ... up to 10,000 rows per batch ...
) AS data(id, short_url)
WHERE url_shortener.id = data.id;
```
__Table with inserted data__
![Table with 1000 rows](https://github.com/hs-4419/URL-Shortener/blob/main/Images/1000%2B%20rows.png)
## 4) Analysis of table post 1K insertion
__Time Taken__
![Time taken for 1K insertion](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Time%20taken%20for%201000%2B%20rows.png)

__Space Taken__
![Space taken by 1K rows](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Table%20size%20with%201000%2B%20rows.png)
## 5) Time and Space post 1M insertions
![Time taken for 1M insertion](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Time%20taken%20for%201M%20rows.png)
![Space taken by 1M+ rows](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Table%20size%20with%201M%2B%20rows.png)

## 6) Time and Space post 10M insertions
![Time taken for 10M insertion](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Time%20taken%20for%2010M%20rows.png)
![Space taken by 10M+ rows](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Table%20size%20with%2010M%2B%20rows.png)

## 7) Time to fetch 5 original url from short url
![Time to fetch 5 original url from short url](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Time%20taken%20to%20get%205%20original_url%20from%20short_url.png)
## 8) Stress Testing -- Ran above query 1M times
![Time taken for stress testing](https://github.com/hs-4419/URL-Shortener/blob/main/Images/Stress%20testing%201M%20retrieval.png)


