sql_always_where: |
  {% if maven_users._eid contains _user_attributes['eid'] %}
    ${user_details_v1.tier_hierarchy} like '%{{ maven_users._tier5managerseid }}%'
  {% else %}
    {% if _user_attributes['eid'] in ['1606469826','0585259858','0905024791','4797182232','4750902532','3200316416'] %}
      1=1
    {% else %}
      ${user_details_v1.tier_hierarchy} like '%{{_user_attributes['eid']}}%'
    {% endif %}
  {% endif %}