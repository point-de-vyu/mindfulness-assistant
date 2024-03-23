CREATE OR REPLACE FUNCTION add_new_user(
	_username TEXT,
    _first_name TEXT,
    _last_name TEXT,
    _token VARCHAR(64)
)
RETURNS BOOL AS $$
DECLARE _id BIGINT;
DECLARE _date_regitered DATETIME;
BEGIN
	_id = generate_user_id();
	_date_regitered = NOW();
	INSERT INTO users VALUES (_id, _username, _first_name, _last_name, _date_regitered);
	INSERT INTO user_tokens VALUES (_id, _token);
	RETURN true;
END;
$$ LANGUAGE plpgsql;