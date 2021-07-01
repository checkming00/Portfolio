select location,date,total_cases/population*100 as Infect_Rate
from covid_deaths
where continent is not null and location in ('Australia','Canada','India','United States','United Kingdom')
order by location,date