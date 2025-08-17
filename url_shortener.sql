create database backend;

-- \c backend

create table url_shortener(
	id serial primary key,
	original_url text,
	short_url varchar(6) unique,
	created_at timestamptz default now()
);
