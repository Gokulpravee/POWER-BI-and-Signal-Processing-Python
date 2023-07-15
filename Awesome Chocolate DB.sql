select * from sales;

select SaleDate, Amount, Customers from sales;
select Amount, Customers, GeoID from sales;

select SaleDate, Amount, Boxes, Amount/Boxes from sales;
select SaleDate, Amount, Boxes, Amount/Boxes as 'Amount per box' from sales;

select * from sales
where  amount > 10000
order by Amount desc;

select * from sales
where geoid = 'G1'
order by PID, Amount desc;

select * from sales
where Amount > 10000 and SaleDate >= '2022-01-01';

select SaleDate, Amount from sales
where Amount > 10000 and year(SaleDate) = '2022'
order by Amount desc;

-- i wanna check the box values from 0 to 50 range --
-- two types of method is there --
-- type one this --
select * from sales
where Boxes > 0 and Boxes <= 50;
-- type two --
select * from sales
where Boxes between 0 and 50;

-- weekday function sql return 0-mon,1-tue,2-wed-,3-thu,4-fri,5-sat,6-sun --
select SaleDate, Amount, Boxes, weekday(SaleDate) as 'Day of Week'
from sales
where weekday(SaleDate) = 4; -- 4 mention friday --

-- i am gonna extract people table --
select * from people;

select * from people
where team = 'Delish' or team = 'Jucies';

-- another way method we may write querey for above the method --
-- 'in' function is add multiple condotion -- 
select * from people
where team in('Delish','Jucies');

-- pattern macthing --
-- using 'like' func i wanna return the name behinning from 'B' --
select * from people
where Salesperson like 'B%'; -- % means anything --
-- %B% this method is particular which are words contains B letter anything --
select * from people
where Salesperson like '%B%'; -- this is a 'like' operator

-- i write one condition for amount catefory for sales table --
-- using case func --
select SaleDate, Amount,
		case 	when Amount < 1000 then 'Under 1k'
				when Amount < 5000 then 'Under 5k'
                when Amount < 10000 then 'Under 10k'
			else '10k or more'
		end as 'Amount as category'
from sales;



-- JOIS --

select * from sales;

select * from people;


-- JOIN --
select sales.SaleDate, sales.Amount, p.Salesperson, sales.SPID, p.spid
from sales
join people p on p.SPID = sales.SPID;


-- LEFT JOIN --
select sales.SaleDate, sales.Amount, pr.Product
from sales
left join products pr on pr.PID = sales.PID;



-- Multiple Joins --
select sales.SaleDate, sales.Amount, p.salesperson, pr.Product, p.team
from sales
join people p on p.spid = sales.SPID
join products pr on pr.PID = sales.PID;


-- in joins i am gonna add some conditions --
select sales.SaleDate, sales.Amount, p.salesperson, p.team, pr.product
from sales
join people p on p.SPID = sales.SPID
join products pr on pr.PID = sales.PID
join geo g on g.GeoID = sales.GeoID
where sales.Amount < 500
-- under 500 for specific team --
and p.Team = 'Delish' -- under 500 in delish team --
and g.Geo in('New Zeland','India')
order by SaleDate;

-- GROUP BY --
select geoid, sum(amount), avg(amount), sum(Boxes), avg(Boxes)
from sales
group by GeoID;

select * from geo;

-- extracting geo table to find sum,avg, from geo --
select g.geo, sum(amount), avg(amount), sum(boxes)
from sales
join geo g on sales.GeoID = g.GeoID
group by g.Geo;

-- get the data from people and product table --
select pr.category, p.Team, sum(Boxes), sum(Amount)
from sales
join people p on p.spid = sales.spid
join products pr on pr.pid = sales.pid
where p.Team <> ''
group by pr.category, p.Team;


-- total amount by top 10 products --
select pr.Product, (amount) as 'Total Amount'
from sales
join products pr on pr.PID = sales.PID
group by pr.Product
order by `Total Amount` desc
limit 10;
