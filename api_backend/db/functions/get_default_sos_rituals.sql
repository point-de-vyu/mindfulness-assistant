CREATE OR REPLACE FUNCTION get_default_sos_rituals()
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
			title,
			description,
			url,
			tags
		FROM sos_rituals_default_ids
			JOIN sos_rituals USING(id)
			JOIN sos_categories ON sos_rituals.category_id = sos_categories.id
			JOIN sos_situations ON sos_rituals.situation_id = sos_situations.id
	);
END;
$$ LANGUAGE plpgsql;