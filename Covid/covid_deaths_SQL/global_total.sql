select sum(total_cases) as World_Cases,
    sum(total_deaths) as World_Deaths
from (select distinct [location],max(coalesce([total_cases],0)) over(partition by [location]) as total_cases,
    max(coalesce([total_deaths],0)) over(partition by [location]) as total_deaths
from [covid_deaths]
where [continent] is not null) as [t]