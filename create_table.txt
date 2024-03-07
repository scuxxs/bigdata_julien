create table student(
id string,
name string,
college string,
major string,
node_name string,
late_level int,
cheat_level int,
poverty_level int,
politics_level int,
academy_level int,
mental_level int,
total_grade int);

create table late(
id string,
latedate string,
node_name string,
reason string);


create table borrow(
id string,
loandate string,
returndate string,
renewtime int,
recalltime int,
isbn string);


create table library(
id string,
type string,
recorddate string,
record_id string);


create table teenagerLearning(
id string,
record_id string,
learn_period string,
learndate string);


create table cost(
id string,
record_id string,
transdate string,
transtime string,
amount float,
type string);


create table gate(
id string,
type string,
record_time string,
is_vocation int);

create table net(
id string,
add_time string,
drop_time string,
total_byte string);


create table poverty(
id string,
level string,
school_year string);


