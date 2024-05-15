sql_always_where: |
  {% if maven_users._eid contains _user_attributes['eid'] %}
    -- If the user's eid is found in the maven_users table,
    -- use the corresponding tier5managerseid for filtering
    ${user_details_v1.eid} = {{ maven_users._tier5managerseid }}
  {% else %}
    -- If the user's eid is not found in the maven_users table,
    -- fall back to the original logic
    ${user_details_v1.tier_hierarchy} like '%{{ _user_attributes['eid'] }}%'
  {% endif %}