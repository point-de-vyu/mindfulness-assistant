-- ADD default data: categories, situations, default rituals

INSERT INTO sos_situations (id, name) VALUES
    (1, 'Stress'),
    (2, 'Anxiety'),
    (3, 'Anger');


INSERT INTO sos_categories (id, name) VALUES
    (1, 'Meditation'),
    (2, 'Breathing exercise'),
    (3, 'Affirmation');


INSERT INTO sos_rituals (id, category_id, situation_id, title, description, url) VALUES
    (3000129241702033816, 2, 1, 'Physiological sigh', 'Take a long breath in, then another, shorter one, again through the nose. Then slowly exhale through the mouth (or nose, if you prefer). Repeat several times.', 'https://www.vastdiversity.com/wp-content/uploads/2023/03/Huberman-physiologic-sigh.png'),
    (3000760721702034141, 1, 2, 'Grounding technique', 'Try this simple meditation, breathe, visualize.', 'https://youtu.be/26ylqdGkd_g?si=QutWLsyXHYra3PAL'),
    (3000453741702034192, 1, 2, 'Grounding technique', 'If your mind is racing with thoughts, try this meditation.', 'https://youtu.be/LgRd1Mzhb_Q?si=W5GaqUJsiq7Kuokp'),
    (3000685801702034286, 1, 2, 'Reset your mind', 'This is a quick Focus Reset Meditation from Headspace.', 'https://youtu.be/QtE00VP4W3Y?si=7yLViGmoQqrtt4m9'),
    (3000125081702034357, 3, 3, 'Let go of anger', 'Listen to the video and imagine it is you saying these words to yourself.', 'https://youtu.be/CBGGDPc1sUE?si=6bEwea861EkgghAQ&t=38'),
    (3000556251702034486, 2, 1, 'Belly breathing', 'Use this practice to feel your body and regain calm', 'https://youtu.be/OXjlR4mXxSk?si=g77CchMyg4IWeLWg&t=75'),
    (3000721381702048768, 1, 1, 'Basic Headspace meditation (10min)', 'Relax and scan your body.', 'https://youtu.be/sG7DBA-mgFY?si=bykTjE8ParXXdDNB'),
    (3000584191702058496, 1, 2, 'Headspace release Stress and Anxious Thoughts', 'Spend 8 minutes meditating, letting go of the anxious thoughts.','https://youtu.be/nFkHV7LfVUc?si=Uvjp-h-xv_6QFrdP');


INSERT INTO sos_rituals_default_ids (id) VALUES
    (3000129241702033816),
    (3000760721702034141),
    (3000453741702034192),
    (3000685801702034286),
    (3000125081702034357),
    (3000556251702034486),
    (3000584191702058496);


-- ADD a test user

INSERT INTO users(id, username, first_name, last_name) VALUES (
	1000470011703256448, '@test_user', 'Jane', 'Doe'
);

INSERT INTO user_tokens(user_id, token) VALUES (
	1000470011703256448, '7ad67dbd1856b031af3e529e0c5755a2542efe7b0a0aba385c5660899986bce7'
);