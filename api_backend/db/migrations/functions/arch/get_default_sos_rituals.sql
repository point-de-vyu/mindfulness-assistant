CREATE OR REPLACE FUNCTION get_default_sos_rituals(_category_id INT, _situation_id INT)
RETURNS TABLE(
	id BIGINT,
	category VARCHAR(30),
	situation VARCHAR(50),
	title TEXT,
	description TEXT,
	url TEXT,
	tags JSON
) AS $$
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
$$ LANGUAGE plpgsql;