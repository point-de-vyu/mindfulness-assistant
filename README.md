### What is this project about?

Mindfulness is somewhat of a buzzword these days, and still many people (including myself) often get caught up in negative emotions, ruminations and traumatic memories. 

There are lots of apps out there designed to help, but I realised that when I open my phone there are so many apps fighting for my attention that it's extremely difficult to remember what I unlocked my screen for - so I failed to consistently use any of them.

Also, there is a problem of choice. Isn't it nearly impossible to make choices when you are overwhelmed? It is for me. I often end up switching to social media to escape the emotions that overwhelm me, and so I fail to help myself.

So I decided to develop a tool that'll better suit my needs.

### How does it work?

Coming from the domain of chatbot development, I decided to develop a personal assistant for this purpose.
I, like many people, always have Telegram open on any device. So I developed a telegram bot that I can quickly use when needed. It actually helped me reduce browsing through apps and pages

At the moment, there is just one simple flow, I called it `sos`. Having typed a `/sos` command:
- you'll get to recognise the emotion causing trouble
- the bot will suggest an exercise (a meditation, a breathing exercise, or an affirmation) to deal with it

Upon completion, you can reflect on how this exercise went, what changed in your mind and body, and journal your thoughts. 
The rituals that worked best for you can be added to favourites. 

![Demo](flow_showcase.gif "Demo")

Even though I developed it for myself, I believe it can benefit other people too, so I made it public: https://t.me/mindfulness_assist_bot

### Technology stack


🐋 Docker

⚡ FastAPI

🗄️ PostgreSQL

🧙 SQLAlchemy

✉️ AIOgram

### What's to come? 

This is not going to be all!
My top priority now is to introduce the ability to create user's own sos rituals.

Besides that, I have a lot of ideas that I'd love to implement, among those:

- help with procrastination and willpower using the idea of [implementation intention](https://en.wikipedia.org/wiki/Implementation_intention)
- more journaling (maybe mental state, sleep, nutrition)
- performing analytics and making reports on demand
