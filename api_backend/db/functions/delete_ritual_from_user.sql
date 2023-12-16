CREATE OR REPLACE FUNCTION delete_ritual_from_user_data(_user_id BIGINT, _ritual_id BIGINT)
RETURNS BOOL AS $$
	DECLARE _is_custom_ritual BOOL;
	BEGIN
		IF _ritual_id IN (SELECT id FROM sos_rituals_default_ids)
		THEN _is_custom_ritual = false;
		ELSE _is_custom_ritual = true;
		END IF;

		DELETEFROM user_sos_ritual
		WHERE user_sos_ritual.user_id = _user_id AND user_sos_ritual.ritual_id = _ritual_id;

		IF _is_custom_ritual
		THEN
			DELETE FROM sos_rituals
			WHERE sos_rituals.id = _ritual_id;
		END IF;
		RETURN true;
	END;
LANGUAGE plpgsql;
