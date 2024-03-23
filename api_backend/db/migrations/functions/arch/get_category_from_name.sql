CREATE OR REPLACE FUNCTION get_category_id_from_name(_category VARCHAR(30))
RETURNS INT AS $$
DECLARE _category_id INT;
BEGIN
	_category_id = (
		SELECT id FROM sos_categories WHERE name = _category
	);
	RETURN _category_id;
END;
$$ LANGUAGE plpgsql;