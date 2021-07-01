select [location],max(cast([total_deaths] as int)) as Deaths
from [covid_deaths]
where [continent] is null and location not like '%world%' and location not like '%inter%'
group by [location]
order by Deaths desc