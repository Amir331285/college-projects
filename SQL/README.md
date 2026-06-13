

# 1. Create Tables


```sql
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
```

> Important parts: 
> 	 grade decimal(4,2)  in scpt table
> 	 primary key(stid,coid,prid) in scpt table
> 	 nvarchar support persian text
> 	 All refrences must have on delete and on update
> 	 
> 

# 2. Insert  

```sql 
insert into department values
('d1','computer','1111'),
('d2','electronic','1122'),
('d3','omran','1133'),
('d4','sazeh','1144'),
('d5','varzesh','1155'),
('d6','mecanic','1166'),
('d7','it','1177' );

```


# 3. Update 

```sql 
UPDATE student
SET age = 30
   WHERE STID = 1403100;
```

# 4. Delete

```sql
 Delete from student where STID = 1403100;
```


# 5. Select

## 1. select all fields

```sql
 select * from student
```

## 2. select explictly 

```sql 
 select STID as ID , age from student
```


# 6. Wildcards

### summary Table

| Wildcard | Description                                  | Example          |
| -------- | -------------------------------------------- | ---------------- |
| `%`      | Any string of zero or more characters        | `LIKE 'bl%'`     |
| `_`      | Any single character                         | `LIKE '_n%'`     |
| `[]`     | Any single character within the range or set | `LIKE '[a-f]%'`  |
| `[^]`    | Any single character not in the range or set | `LIKE '[^a-f]%'` |

 

# 7. Group

> **What is group by ?**  You can group by records by specifc field and the records with same field value will be grouped by. and you use functions like ==count== for all value type and  ==avg==, ==max== and ==min== for number value types, But you can select the field that records got grouped by cause all grouped records share same value for that 

```sql

 SELECT count(*) as countOfDocuments, STMAJOR from Student group by STMAJOR

```

### Condition after grouped by

You can use having to filter the table after group so you can use Functions like ==avg==, ==min== ,==max== and ==count==. and use where before group to filter documents simply 

```sql

 SELECT count(*) as countOfDocuments, STMAJOR from Student
  where  STMAJOR <> 'Computer'
  group by STMAJOR 
  having count(*) > 1

```


   <div align="center">
      <img src="https://github.com/mahdijz5/college-projects/blob/main/SQL/Pasted%20image%2020260613224720.png">
    </div>

# 9. Operators

| Operator        | Logic                                              | Includes Duplicates? |
| --------------- | -------------------------------------------------- | -------------------- |
| **`UNION`**     | All distinct rows from both queries                | No                   |
| **`UNION ALL`** | All rows from both queries                         | Yes                  |
| **`INTERSECT`** | Rows common to both queries                        | No                   |
| **`EXCEPT`**    | Rows in the first query that are not in the second | No                   |


# 10. Joins

## Existing tables 

### Student table

| STID | NAME  | AGE |
| ---- | ----- | --- |
| 10   | Ali   | 12  |
| 11   | Mety  | 22  |
| 12   | Parsa | 11  |


### Grade table

| ID  | STID | Grade |
| --- | ---- | ----- |
| 1   | 10   | 19    |
| 2   | 11   | 11    |
| 3   | 16   | 14    |
Third record is for non-existed student
## 1. Left Join

```sql 
Select * from student left join grade on grade.STID = student.STID 
```
 
 Result : 

| STID | NAME  | AGE | ID   | STID | Grade |
| ---- | ----- | --- | ---- | ---- | ----- |
| 10   | Ali   | 12  | 1    | 10   | 19    |
| 11   | Mety  | 22  | 2    | 11   | 11    |
| 12   | Parsa | 11  | null | null | null  |

##  2. Right Join`

```sql 
Select * from student RIGHT join grade on grade.STID = student.STID 
```
 
 Result : 

| STID | NAME | AGE  | ID  | STID | Grade |
| ---- | ---- | ---- | --- | ---- | ----- |
| 10   | Ali  | 12   | 1   | 10   | 19    |
| 11   | Mety | 22   | 2   | 11   | 11    |
| null | null | null | 3   | 16   | 14    |

## 3. Join OR Inner Join

```sql 
Select * from student join grade on grade.STID = student.STID 
```

| STID | NAME | AGE | ID  | STID | Grade |
| ---- | ---- | --- | --- | ---- | ----- |
| 10   | Ali  | 12  | 1   | 10   | 19    |
| 11   | Mety | 22  | 2   | 11   | 11    |


   <div align="center">
      <img src="https://github.com/mahdijz5/college-projects/blob/main/SQL/Pasted%20image%2020260613224720.png">
    </div>

# 11. Temp Tables 

```sql
CREATE TABLE #TopStudents 
( 
 STID INT,
 Name NVARCHAR(50),
 AverageGrade FLOAT
);
```


1. All temp tables are stored in Temp database. no matter from which database you created it will get stored in same location
2. You can use it like normal table
3. Get deleted after database/system got shutdown 

# 12. View 

 Basically you save query like table 

```sql 
CREATE VIEW scptWithGradeHigherThanTen AS 
select STID from  scpt 
where grade > 10
```

Then you can instead of : 

```sql 
select STID from  scpt 
where grade > 10
```

do : 

```sql
select * from scptWithGradeHigherThanTen
```

they will have same result.


Another use case : 

```sql
select * from student where STID  IN
(
select STID from  scpt 
where grade > 10
)
```

You can: 

```sql
select * from student where STID  IN
(
select STID from scptWithGradeHigherThanTen
)
```


# 13. Trigger

> By trigger you can run query after specific action occurred.
> action could be `Insert`, `update` and `delete`

```Sql
CREATE TRIGGER trg_Students_Insert
ON students
AFTER INSERT /* Could be also : UPDATE, DELETE */
as BEGIN 
	/* The query you wanna get executed if student got insert */
END
```

Example : 
Set grade of students to 10 if it was below 10 ==When scpt Added or Updated==

```sql
CREATE TRIGGER trg_Students_Insert
ON scpt
AFTER INSERT, Update /* Added or Updated */
as BEGIN 
	UPDATE scpt set grade = 10 where grade < 10
END

```


   <div align="center">
      <img src="https://github.com/mahdijz5/college-projects/blob/main/SQL/Pasted%20image%2020260613230551.png">
    </div>
