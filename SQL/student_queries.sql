create database university

use university
go

create table department(
deid char(10) not null primary key,
detitle varchar(50) not null,
dephone char(10) not null
);

create table student(
stid char(10) not null primary key,
stname varchar(50) not null,
stlevel varchar(50) not null,
stmjr varchar(50),
deid char(10),
check (stlevel = 'bs' or stlevel = 'ms' or stlevel = 'phd'),
foreign key (deid) references department(deid)
on delete cascade
on update cascade  
);


create table course(
coid char(10) not null primary key,
cotitle varchar(50) not null,
credit varchar(50),
cotype varchar(50),
deid char(10),
foreign key (deid) references department(deid)
on delete cascade
on update cascade
)

create table professor(
prid char(10) not null primary key,
pname varchar(50) not null,
prank varchar(50),
pfrom varchar(50),
deid char(10),
foreign key (deid) references department(deid)
on delete cascade
on update cascade
)

create table scpt(
stid char(10),
coid char(10),
prid char(10),
tr char(4),
yr char(4),
grade decimal(4,2),
primary key(stid,coid,prid),
foreign key (stid) references student(stid)
on delete no action
on update no action,
foreign key (coid) references course(coid)
on delete no action
on update no action,
foreign key (prid) references professor(prid)
on delete no action
on update no action, 
)


insert into department values
('d1','computer','1111'),
('d2','electronic','1122'),
('d3','omran','1133'),
('d4','sazeh','1144'),
('d5','varzesh','1155'),
('d6','mecanic','1166'),
('d7','it','1177' );

insert into student values
('1400123','reza zadeh','ms','computer','d1'),
('1400124','hasani','ms','computer','d1'),
('1400125','mohammadi','bs','computer','d1'),
('1400126','saeidi','ms','mecanic','d6'),
('1400127','hashemi','ms','varzesh','d5'),
('1400128','khatami','bs','computer','d1'),
('1400129','hatami','bs','it','d7'),
('1400130','saberi','ms','varzesh','d5'),
('1400131','khabaz','ms','computer','d1'),
('1400132','koohestani','phd','computer','d1'),
('1400133','rahmani','ms','it','d7'),
('1400134','rahimi','ms','sazeh','d4'),
('1400136','mardani','ms','omran','d3'),
('1400135','moradzadeh','ms','sazeh','d4'),
('1400137','hasanzadeh','ms','electronic','d2'),
('1400138','dehaki','phd','computer','d1');

insert into course values
('11111','az payegah','2','p','d1'),
('11321','payegah','2','t','d1'),
('11331','python','3','t','d1'),
('11344','madar','2','t','d2'),
('11398','electronic','3','t','d2'),
('11345','electronic','3','t','d6'),
('11309','valibal','2','p','d5'),
('11376','sakhteman','3','t','d4'),
('11365','omran','3','t','d3');

insert into professor values
('11133','mohamadi','phd','1390','d1'),
('11144','hamidzadeh','phd','1380','d1'),
('11155','bagheri','phd','1400','d6'),
('11166','noori','phd','1390','d2'),
('11177','hamidi','phd','1388','d3'),
('11188','hayati','phd','1395','d5'),
('11199','rahimi','phd','1401','d4');

insert into scpt values
('1400123','11111','11133','1', '1402',' 20.00'),
('1400124','11331','11144','1', '1390',' 20.00'),
('1400125','11331','11144','2', '1402',' 18.75'),
('1400136','11365','11177','1', '1402',' 15.25'),
('1400137','11345','11166','1', '1402',' 19.30');

select * from department
select * from student
select * from course
select * from professor
select * from scpt

--delete trigger
create table logs(
id_log int identity primary key,
stid int,
stname varchar(50),
date_time datetime
)

create trigger del_trig on student
after delete
as
begin
insert into logs(stid,stname,date_time)
select stid,stname,GETDATE() from deleted
end

insert into student values
('1400269','reza zadeh','ms','computer','d1');

delete student where stid = '1400269'

select * from logs
select * from sys.triggers
exec sp_helptext 'del_trig'
exec sp_helptrigger 'student'

-- insert trigger
create table insert_logs(
id_log int identity not null primary key,
log_message varchar(100)
)

create trigger ins_trigger on student
after insert
as begin
insert into insert_logs(log_message)
values ('someone has been added to student table.')
end

insert into student values
('1400371','reza zadeh','ms','computer','d1');

select * from insert_logs

-- temporary table
-- دانشجویان با معدل بالای 17 در جدول موقت
create table #top_student(
stid char(10),
avg_grade decimal(4,2)
)

insert into #top_student
select stid, avg(grade)
from scpt
group by stid
having avg(grade) > 17;

select * from scpt
select * from #top_student

-- view

-- یک ویو با نمایش نام دانشجو، نام در س و نمره
create view vw_student
as select
student.stname,
course.cotitle,
scpt.grade
from student
join scpt
on student.stid = scpt.stid
join course
on course.coid = scpt.coid;

select * from vw_student

-- join

-- نمایش نام دانشجویان به همراه نام دپارتمان آن‌ها
select student.stname, department.detitle
from student
join department
on student.deid = department.deid

-- نمایش نام درس‌ها به همراه دپارتمان ارائه‌دهنده
select course.cotitle, department.detitle
from course
join department
on course.deid = department.deid

-- نمایش نام دانشجویان به همراه نمره‌های ثبت شده
select student.stname, scpt.grade
from student
join scpt
on student.stid = scpt.stid

-- نام دانشجو و نام درس اخذ شده
select student.stname, course.cotitle
from student
join scpt
on student.stid = scpt.stid
join course
on scpt.coid = course.coid

-- نام دانشجو، نام درس و نمره
select student.stname, course.cotitle, scpt.grade
from student
join scpt
on student.stid = scpt.stid
join course
on scpt.coid = course.coid

-- نام دانشجو، نام استاد و نام درس
select student.stname, professor.pname, course.cotitle
from student
join professor
on student.deid = professor.deid
join course
on professor.deid = course.deid

-- نام دانشجو، نام درس، نام استاد و نمره
select student.stname, course.cotitle, professor.pname, scpt.grade
from student
join scpt
on student.stid = scpt.stid
join course
on scpt.coid = course.coid
join professor
on scpt.prid = professor.prid 

-- دانشجویان رشته کامپیوتر به همراه دروس اخذ شده
select student.stname, course.cotitle
from student
join scpt
on student.stid = scpt.stid
join course
on course.coid = scpt.coid
where stmjr = 'computer' 

-- دانشجویانی که نمره بالاتر از 18 گرفته‌اند به همراه نام درس
select student.stname, course.cotitle,scpt.grade
from student
join scpt
on student.stid = scpt.stid
join course
on course.coid = scpt.coid
where grade > '18'

--نام دانشجو، نام دپارتمان و نام استاد
select student.stname, department.detitle, professor.pname
from scpt
join student
on student.stid = scpt.stid
join professor
on scpt.prid = professor.prid
join department
on student.deid = department.deid


-- left join

-- نمایش همه دانشجویان حتی اگر هیچ درسی اخذ نکرده باشند
select student.stname, scpt.grade
from student
left join scpt
on student.stid = scpt.stid
