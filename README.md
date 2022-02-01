
# Blog Post API
## Summary
Simple API program that parses and analyzes posts from an publicly available API. This project was done on my own time for learning purposes. It incorperates REST API techniques, multi-threading and optimized algorithms (done with O(nlogn)).

## Setup (Windows)
- This project requires a few features to be installed before it can run.
- To install all necessary programs, run `setup.bat` in the `../blog_posts` project directory.

## Setup (Linux)
- This project requires a few features to be installed before it can run.
- To install all necessary programs, run `./setup_env.sh` in the `../blog_posts` project directory.

## Manual setup 
- This project requires a few features to be installed before it can run.
- Make sure Python and Pip is installed on your machine.
- Install the requirements in requirements.txt using `pip install -r  requirements.txt` 

## Running the app
Default port number of the API is 5050. Thus, once you run `python api_post.py` and enter `localhost:5050` on your browser. If all is well, you should see a page with the text "Hello", confirming that you have setup everything properly.

You can then visit local `localhost:5050/swagger` to view all the available routes in the API.

## Running testcases
Running test cases can be done by executing this command: `python -m pytest` in the `blog_posts` directory.
