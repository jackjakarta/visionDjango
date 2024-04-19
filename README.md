# Vision Web App w/ Django

Access the app **[here](https://visionbrain.xyz)**.

## Intro

This Django app uses GPT-4 and OpenCV to analyze video frames, generating a context-aware response based on these frames.

## Navigation

- [Features](#features)
- [Installation](#installation)
  - [MySQL Database](#database-setup)
  - [Django Server](#django-server)
  - [Celery and Redis](#celery-and-redis)
- [Technologies](#technologies-used)

## Features

- **Video Frame Analysis:** Utilizes OpenCV to analyze each frame of the video and pass it to the OpenAI API
- **GPT-4:** Uses the vision capabilities of GPT-4 to interpret the analyzed frames, ensuring responses are contextually relevant.
- **Custom Instructions:** Offers the flexibility to tailor the narration style to fit the video’s tone and audience by giving custom instructions to the model.
- **Text-To-Speech:** Generates Text-To-Speech audio files from the narration text using OpenAI or ElevenLabs TTS models.

## Installation

Make sure you have `libgl1-mesa-glx` installed on your machine. This is needed for **OpenCV**.

```bash
sudo apt install libgl1-mesa-glx
```

### Database Setup

**Skip this step if you already have a MySQL server or other database set up.*

***Adjust your `settings.py` file accordingly if you are not using MySQL.*

The easiest way to set up a ***MySQL*** server locally is with `docker`. Adjust the command to your needs. This
command will use `root` as the only user and the password set in the run command as env variable.

```commandline
docker run -d \ 
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=your-password-here \
-e MYSQL_DATABASE=your-db-name-here \
--name mysql-db \
mysql:latest
```

You can connect to the `mysql` or `bash` shells with the following commands.

- MySQL Shell

```commandline
docker exec -it mysql-db mysql -u root -p
```

- Bash Shell
```commandline
docker exec -it mysql-db bash
```

### Django Server

1. Create and activate a virtual environment.

    ```commandline
    python3 -m venv env && \
    . env/bin/activate
    ```

2. Install dependencies with pip.

    ```commandline
    pip3 install -r requirements.txt
    ```

3. Set up your environment variables by using the template and information at `.env.default`.


4. Run database migrations.

    ```commandline
    python3 manage.py migrate
    ```
   
5. Collect static files.
   
    ```commandline
    python3 manage.py collectstatic
    ```
   
   **You don't need to run this if your using the development server and serving static files locally. Only if you use 
   S3 storage or a production server (e.g. gunicorn). Check `.env.default` file.*


6. Run the development server.

    ```commandline
    python3 manage.py runserver
    ```

If everything was set up correctly you should be able to access 
the app at: [http://localhost:8000](http://localhost:8000)

### Celery and Redis

You need to set up a ***Redis*** database in order for celery to work with the app which is used to process videos asynchronously.
The server will start even without this and can be accessed but videos won't process.

1. You can use `docker` to run a Redis instance locally very easily.

   ```commandline
   docker run -d -p 6379:6379 --name my-redis redis
   ```

2. Start a `celery` worker. You can adjust the parameters as needed.

   ```commandline
   celery -A vision_app worker -l info --concurrency=1 --pool=solo 
   ```

## Technologies Used
- [Django](https://github.com/django/django)
- [MySQL](https://www.mysql.com/)
- [Redis](https://redis.io/)
- [Celery](https://github.com/celery/celery)
- [OpenCV](https://github.com/opencv/opencv-python)
- [OpenAI](https://github.com/openai/openai-python)
