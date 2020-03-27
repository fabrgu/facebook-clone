# facebook-clone
A facebook clone.

# Features
 * Sign up and Log in to the web app.
 * Search for users to friend
 * View your friend's posts
 * Comment on your friend's posts

# How to Run locally
Have the following installed in your machine:
 * Python version 3.6.9
 * Pip version 20.0.2 (pip3)
 * Git
 * PostgreSQL

Steps:
  Navigate to the facebook-clone directory on the command line:
  
 ```
cd facebook-clone
 ```
 
 Create the facebook-clone PostgreSQL db by running on the command line:

 ```
createdb facebook-clone
 ```

 Create the tables in the facebook-clone db by running on the command line:

 ```
 psql facebook-clone < database.sql
 ```

 Install virtualenv if it's not available on your machine already.

 ```
 pip3 install virtualenv
 ```

 Create a virtual environment and install all the python libraries required 
 by the project.

 ```
 virtualenv env
 ```
 
 ```
 source env/bin/activate
 ```

 ```
 pip3 install -r requirements.txt
 ```

Now you can run the app locally by running on the command line:

```
python3 server.py
```
# To Test

To run any unit tests, while your virtual environment is active, run the following on the command line:

```
python3 tests.py
```

# Planning
 * Visuals and Models: https://drive.google.com/file/d/1fC5P8wuw9uWl2hyoC6FxpASm_0x-UzSu/view?usp=sharing

