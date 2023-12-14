CREATE OR REPLACE FUNCTION get_user_sos_rituals(_user_id BIGINT, _category_id INT, _situation_id INT)
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
$$ LANGUAGE plpgsql;
