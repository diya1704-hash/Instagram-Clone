CREATE DATABASE instagramclone;
use instagramclone;

CREATE TABLE users(
   id INT AUTO_INCREMENT PRIMARY KEY,
   username varchar(50),
   email varchar(100),
   password varchar(255)
   );

CREATE TABLE posts(
   id int AUTO_INCREMENT PRIMARY KEY,
   user_id int,
   image_url text,
   caption text,
   created_at timestamp default CURRENT_TIMESTAMP
);

CREATE TABLE followers(
   follower_id int,
   following_id int
);

CREATE TABLE likes(
  user_id int,
  post_id int
);

CREATE Table comments(
   id int AUTO_INCREMENT PRIMARY KEY,
   user_id int,
   post_id int,
   text TEXT
);

