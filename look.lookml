sql_always_where: |
  {% if maven_users._eid contains _user_attributes['eid'] %}
    ${user_details_v1.tier_hierarchy} like '%{{ maven_users._tier5managerseid }}%'
  {% else %}
    {% if _user_attributes['eid'] == '1606469826' or
          _user_attributes['eid'] == '0585259858' or
          _user_attributes['eid'] == '0905024791' or
          _user_attributes['eid'] == '4797182232' or
          _user_attributes['eid'] == '4750902532' or
          _user_attributes['eid'] == '3200316416' %}
      1=1
    {% else %}
      ${user_details_v1.tier_hierarchy} like '%{{_user_attributes['eid']}}%'
    {% endif %}
  {% endif %}