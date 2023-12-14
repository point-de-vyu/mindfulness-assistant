CREATE OR REPLACE FUNCTION add_custom_sos_ritual(
	_user_id BIGINT,
	_category_id INT,
	_situation_id INT,
	_title TEXT,
	_description TEXT,
	_url TEXT,
	_tags JSON
)
    RETURNS BIGINT AS $$

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
$$ LANGUAGE plpgsql;