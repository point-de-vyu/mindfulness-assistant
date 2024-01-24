CREATE OR REPLACE FUNCTION add_new_user(
    _username TEXT,
    _first_name TEXT,
    _last_name TEXT,
    _client_id INT,
    _user_id_from_client INT
    )
    RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE _id BIGINT;
DECLARE _date_regitered DATE;
BEGIN
	_id = generate_user_id();
	_date_regitered = NOW();
	INSERT INTO users VALUES (_id, _username, _first_name, _last_name, _date_regitered);
	INSERT INTO clients_users VALUES(_client_id, _user_id_from_client, _id);
	RETURN _id;
END;
$$;


CREATE OR REPLACE FUNCTION generate_user_id() RETURNS bigint
    LANGUAGE plpgsql STABLE
    AS $$BEGIN
	RETURN 1000000000000000000 + FLOOR(RANDOM() * 99999) * 10000000000 + CAST(EXTRACT(epoch FROM current_timestamp) AS INTEGER);
END;
$$;