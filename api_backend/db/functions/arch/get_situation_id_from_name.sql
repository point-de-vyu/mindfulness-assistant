CREATE OR REPLACE FUNCTION get_situation_id_from_name(_situation VARCHAR(50))
RETURNS INT AS $$
DECLARE _situation_id INT;
BEGIN
	_situation_id = (
		SELECT id FROM sos_situations WHERE name = _situation
	);
	RETURN _situation_id;
END;
$$ LANGUAGE plpgsql;