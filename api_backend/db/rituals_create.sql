CREATE TABLE IF NOT EXISTS sos_categories(
	id serial PRIMARY KEY UNIQUE NOT NULL,
	name VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sos_situations(
	id serial PRIMARY KEY UNIQUE NOT NULL,
	name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS sos_rituals(
	id BIGINT PRIMARY KEY UNIQUE NOT NULL,
	category_id INT NOT NULL,
	situation_id INT NOT NULL,
	title TEXT NOT NULL,
	description TEXT NOT NULL,
	url TEXT,
	tags JSON,

	FOREIGN KEY(category_id) REFERENCES sos_categories(id) ON UPDATE CASCADE,
	FOREIGN KEY(situation_id) REFERENCES sos_situations(id) ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS sos_rituals_default_ids(
	id BIGINT PRIMARY KEY UNIQUE NOT NULL,

	FOREIGN KEY(id) REFERENCES sos_rituals(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS user_sos_ritual (
	user_id BIGINT NOT NULL,
	ritual_id BIGINT NOT NULL,
	PRIMARY KEY(user_id, ritual_id),
	FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(ritual_id) REFERENCES sos_rituals(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS user_feedback_to_ritual (
	user_id BIGINT NOT NULL,
	ritual_id BIGINT NOT NULL,
	feedback_date TIMESTAMPTZ NOT NULL,
	feedback TEXT NOT NULL,
	FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(ritual_id) REFERENCES sos_rituals(id) ON DELETE CASCADE ON UPDATE CASCADE
);