CREATE FUNCTION public.add_default_sos_ritual(IN category character varying, IN situation character varying, IN title text, IN description text, IN url text DEFAULT NULL, IN tags json DEFAULT NULL)
    RETURNS boolean
    LANGUAGE 'plpgsql'
    VOLATILE
AS $BODY$
DECLARE _rit_id BIGINT = generate_ritual_id();
DECLARE _cat_id INT = (SELECT id FROM sos_categories WHERE name = category);
DECLARE _sit_id INT = (SELECT id FROM sos_situations WHERE name = situation);

BEGIN
	INSERT INTO sos_rituals VALUES (
		_rit_id,
		_cat_id,
		_sit_id,
		title,
		description,
		url,
		tags
	);
	INSERT INTO sos_rituals_default_ids VALUES (_rit_id);
	RETURN true;
END;
$BODY$;

ALTER FUNCTION public.add_default_sos_ritual(character varying, character varying, text, text, text, json)
    OWNER TO postgres;