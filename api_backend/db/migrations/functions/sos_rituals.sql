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

CREATE OR REPLACE FUNCTION add_default_sos_ritual(
    category character varying,
    situation character varying,
    title text,
    description text,
    url text DEFAULT NULL::text,
    tags json DEFAULT NULL::json
    )
    RETURNS boolean
    LANGUAGE plpgsql
    AS $$
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
$$;


CREATE OR REPLACE FUNCTION delete_ritual_from_user_data(_user_id bigint, _ritual_id bigint) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE _is_custom_ritual BOOL;
BEGIN
	IF _ritual_id IN (SELECT id FROM sos_rituals_default_ids)
	THEN _is_custom_ritual = false;
	ELSE _is_custom_ritual = true;
	END IF;

	DELETE FROM user_sos_ritual 
	WHERE user_sos_ritual.user_id = _user_id AND user_sos_ritual.ritual_id = _ritual_id;

	IF _is_custom_ritual
	THEN
		DELETE FROM sos_rituals
		WHERE sos_rituals.id = _ritual_id;
	END IF;
	RETURN true;
END;
$$;


CREATE OR REPLACE FUNCTION generate_ritual_id() RETURNS bigint
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN 3000000000000000000 + floor(random() * 99999) * 10000000000 + cast(extract(epoch from current_timestamp) AS INTEGER);
END;
$$;


CREATE OR REPLACE FUNCTION get_category_id_from_name(_category character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE _category_id INT;
BEGIN
	_category_id = (
		SELECT id FROM sos_categories WHERE name = _category
	);
	RETURN _category_id;
END;
$$;


CREATE OR REPLACE FUNCTION get_default_sos_rituals(_category_id integer, _situation_id integer)
RETURNS TABLE(
    id bigint,
    category character varying,
    situation character varying,
    title text,
    description text,
    url text,
    tags json
    )
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY (
		SELECT
			sos_rituals.id AS id,
			sos_categories.name AS category,
			sos_situations.name AS situation,
			sos_rituals.title,
			sos_rituals.description,
			sos_rituals.url,
			sos_rituals.tags
		FROM sos_rituals_default_ids
			JOIN sos_rituals USING(id)
			JOIN sos_categories ON sos_rituals.category_id = sos_categories.id
			JOIN sos_situations ON sos_rituals.situation_id = sos_situations.id
		WHERE
		(_category_id IS NULL OR sos_categories.id = _category_id)
			AND
		(_situation_id IS NULL OR sos_situations.id = _situation_id)
	);
END;
$$;


CREATE OR REPLACE FUNCTION get_situation_id_from_name(_situation character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE _situation_id INT;
BEGIN
	_situation_id = (
		SELECT id FROM sos_situations WHERE name = _situation
	);
	RETURN _situation_id;
END;
$$;

CREATE OR REPLACE FUNCTION get_user_sos_rituals(
    _user_id bigint,
    _category_id integer,
    _situation_id integer
    ) 
    RETURNS TABLE(
        id bigint,
        category character varying,
        situation character varying,
        title text,
        description text,
        url text,
        tags json
    )
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY (
		SELECT
			user_sos_ritual.ritual_id AS id,
			sos_categories.name AS category,
			sos_situations.name AS situation,
			sos_rituals.title,
			sos_rituals.description,
			sos_rituals.url,
			sos_rituals.tags
		FROM user_sos_ritual
			JOIN sos_rituals ON user_sos_ritual.ritual_id = sos_rituals.id
			JOIN sos_categories ON sos_rituals.category_id = sos_categories.id
			JOIN sos_situations ON sos_rituals.situation_id = sos_situations.id
		WHERE user_sos_ritual.user_id = _user_id
			AND
		(_category_id IS NULL OR sos_categories.id = _category_id)
			AND
		(_situation_id IS NULL OR sos_situations.id = _situation_id)
	);
END;
$$;


CREATE OR REPLACE FUNCTION add_sos_ritual_feedback(
	_user_id BIGINT,
	_ritual_id BIGINT,
	_feedback TEXT
)
RETURNS BOOL
LANGUAGE plpgsql
AS $$
DECLARE _date_logged DATE;
BEGIN
	_date_logged = NOW();
	INSERT INTO user_feedback_to_ritual VALUES (_user_id, _ritual_id, _date_logged, _feedback);
	RETURN TRUE;
END;
$$;