drop table if exists orderes;
create table orderes (
  order_id char(12) primary key,
  order_date date not null,
  order_type boolean not null,
  good_id  char(12) not null,
  status integer not null,
  single_price float not null,
  total_price float not null,
  discount integer not null,
  is_comment boolean not null,
  seller_id char(12) not null,
  buyer_id char(12) not null
);
drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);
