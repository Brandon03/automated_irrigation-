drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    msg_id text,
    year integer not null,
    month integer not null,
    day integer not null,
    name text not null,
    category text not null,
    quantity integer not null,
    price integer not null
);
