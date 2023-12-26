CREATE VIEW default_rituals AS
 SELECT default_sos_rits.id AS ritual_id,
    cats.name AS category,
    sits.name AS situation,
    sos_rits.title,
    sos_rits.description,
    sos_rits.url
   FROM (((sos_rituals sos_rits
     JOIN sos_rituals_default_ids default_sos_rits USING (id))
     JOIN sos_categories cats ON ((sos_rits.category_id = cats.id)))
     JOIN sos_situations sits ON ((sos_rits.situation_id = sits.id)));


CREATE VIEW user_rituals_with_data AS
 SELECT sos_rits.id AS ritual_id,
    users.id AS user_id,
    users.username,
    cats.name AS category,
    sits.name AS situation,
    sos_rits.title,
    sos_rits.description,
    sos_rits.url,
        CASE
            WHEN (sos_rits.id IN ( SELECT sos_rituals_default_ids.id
               FROM sos_rituals_default_ids)) THEN 'is_default'::text
            ELSE 'is_custom'::text
        END AS "case"
   FROM ((((sos_rituals sos_rits
     JOIN user_sos_ritual ON ((sos_rits.id = user_sos_ritual.ritual_id)))
     JOIN users ON ((users.id = user_sos_ritual.user_id)))
     JOIN sos_categories cats ON ((sos_rits.category_id = cats.id)))
     JOIN sos_situations sits ON ((sos_rits.situation_id = sits.id)));