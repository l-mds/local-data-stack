
select *
from {% raw %}{{ ref('my_first_dbt_model') }}{% endraw %}
where id = 1
