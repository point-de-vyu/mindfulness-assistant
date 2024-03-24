CREATE FUNCTION public.generate_ritual_id() RETURNS bigint
    AS $$
BEGIN
	RETURN 3000000000000000000 + floor(random() * 99999) * 10000000000 + cast(extract(epoch from current_timestamp) AS INTEGER);
END;
$$ LANGUAGE plpgsql;