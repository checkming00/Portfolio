with total as (select distinct [location],max(coalesce([total_cases],0)) over(partition by [location]) as total_cases,
    max(coalesce([total_deaths],0)) over(partition by [location]) as total_deaths
from [covid_deaths]
where [continent] is not null)
select t.location,(t.total_cases/c.population) as Infection_Rate,
   (case when t.total_cases=0 then 0
    else t.total_deaths/t.total_cases end) as Death_Rate
from total as t
join covid_deaths as c
on t.location=c.location
where t.total_cases=c.total_cases and t.total_deaths=c.total_deaths