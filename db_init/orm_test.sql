/*
* @Author: moling
* @Date:   2016-05-05 19:58:41
*/

drop database if exists orm_test;

create database orm_test;

use orm_test;

grant select, insert, update, delete on orm_test.* to 'orm'@'localhost' identified by 'test';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;