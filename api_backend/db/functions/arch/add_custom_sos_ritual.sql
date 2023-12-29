CREATE OR REPLACE FUNCTION add_custom_sos_ritual(
    _user_id bigint,
    _category_id integer,
    _situation_id integer,
    _title text,
    _description text,
    _url text,
    _tags json
)
RETURNS bigint
LANGUAGE plpgsql
    AS $$
DECLARE _ritual_id BIGINT = generate_ritual_id();
BEGIN
	INSERT INTO sos_rituals(
		id,
		category_id,
		situation_id,
		title,
		description,
		url,
		tags
	) VALUES(
		_ritual_id,
		_category_id,
		_situation_id,
		_title,
		_description,
		_url,
		_tags
	);
	INSERT INTO user_sos_ritual(user_id, ritual_id) VALUES (_user_id, _ritual_id);
	RETURN _ritual_id;
END;
$$;