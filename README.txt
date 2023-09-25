The main aim for my assignment was to create a mock Social Media site where users can create an account and log in.

1. I created two classes called Info (which stored basic user information such as usernames and passwords) and Blog(which stored all posts made by a user).

2. To store sensitive information, in my case storing passwords, I installed Werkzeug which allows a password to be encrypted via salting and hashing.

3. When a user has registered an email, I created a variable called existing_email whcih cycles through all the emails stored in a class and make sure there isn't one already taken. 