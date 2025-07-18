# What is GSS and why is it deprecated?

GSS stands for General Socket Server. This server was responsible for updating, adding, deleting, and managing all user data in my Bloomia app (which is a private project). Basically, it's meant to handle most of the server-side work for my app.

When I was trying to figure out how I could use Python as my socket server, I first started exploring how to implement Socket.io in Python as a backend server, then I found flask-socketio. In the first few days, it was good, but then other things came into play like authentication, asynchronous tasks, workers, and Gunicorn. Then I realized that Python is not good for backend development. It's a shitty language just for basic educations, mathematicians, AI engineers, and writing small scripts. Its syntax is awfull hard to maintain especially in larger projects, its become impossible work with it.

I'm planning to rewrite and fix all of my code in Node.js. Python was never meant to be a web language, and the community doesn't want that either. There aren't many people in the Python community who want to make scalable backend services.
