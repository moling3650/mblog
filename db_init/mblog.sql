/*
* @Author: moling
* @Date:   2016-05-06 10:51:29
* @Last Modified by:   anchen
* @Last Modified time: 2016-07-14 23:10:07
*/
drop database if exists mblog;

create database mblog;

use mblog;
grant select, insert, update, delete on mblog.* to 'moling'@'localhost' identified by 'www-data';

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

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table oauth (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    unique key `idx_uid` (`user_id`),
    primary key (`id`)
) engine=innodb default charset=utf8;
