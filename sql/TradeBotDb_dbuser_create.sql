create user 'dbuser'@'%' identified by 'password';
create database TradeBotDb;
use TradeBotDb;
create table MainTab (start_point datetime,finish_point datetime,period NVARCHAR(10),step NVARCHAR(5),vol_btc NVARCHAR(50),vol_usd NVARCHAR(50),bal_btc NVARCHAR(50),bal_usd NVARCHAR(50),old_ord NVARCHAR(5),max_usage NVARCHAR(5),margin NVARCHAR(50),per NVARCHAR(5),total_sum NVARCHAR(50),comb_status NVARCHAR(15));
grant all privileges on TradeBotDb.* to 'dbuser'@'%';
flush privileges;
