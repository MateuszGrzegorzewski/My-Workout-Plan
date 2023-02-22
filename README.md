# My Workout Plan

My Workout Plan is a Python Django application that allows users to create professional training plans and search for appropriate exercises for different muscle groups. The project focuses on the backend.

## Project Description

The project consists of two main parts. One is responsible for training plans. Its functionalities are:

- creating customized trainings,
- creating plans,
- adding training results to monitor progress.

The second part of the project is the Musclewiki app. Its functionalities are:

- searching for exercises for specific muscle groups,
- creating muscle groups and exercises but only by admin,
- adding custom exercises by the user.

The application uses technologies such as:

- Django,
- Django RESTFramework,
- HTML/CSS,
- unittest,
- Docker.

Thanks to this project, I acquired skills in using the Django framework and the DjangoRESTFramework. Among other things, I gained experience in creating a complex CRUD system and implementing effective validation and permission mechanisms. What's more, I acquired skills in managing user accounts, including login, registration and logout.

In addition, I was able to build a simple frontend presenting the functionality of the application.

Another aspect was the creation of complete tests to verify the written code.

As for future improvements, I intend to improve account management by implementing features such as resetting passwords and enabling login via email, as well as increasing security. I also plan to refine the front-end of the project to enable a clear way to use the application.

In addition, I intend to add a function to analyze training results, allowing users to determine their progress.

## How to Install the Project

1. Installation of all dependencies for the project:  
   `pip install -r requirements.txt`

2. Create a .env file. An example of a finished file is:

   > DJANGO_SECRET_KEY=super-secret-key123  
   > DEBUG=1  
   > DJANGO_ALLOWED_HOST=127.0.0.1 localhost  
   > POSTGRES_DB=myworkoutplandb  
   > POSTGRES_USER=myworkoutplanuser  
   > POSTGRES_PASSWORD=secretpassword123

3. Run the following command to start the application:
   `docker compose up`

4. Get the ID of the web container by running the following command:
   `docker ps`

5. Enter the web container by running the following command:
   `docker exec -it {id of container} bash`

6. Database migration:  
   `python manage.py migrate`

7. The application will be available at: https://localhost:8000/

## How to run the Project

If you have installed the application in the correct way is enough:  
`docker compose up`

And the application will be available at: https://localhost:8000/

## How to run tests

1. Start the application using the commands in the previous sections.
2. Get the ID of the web container by running the following command:
   `docker ps`
3. Enter the web container by running the following command:
   `docker exec -it {id of container} bash`
4. Run tests with the following command:
   `python manage.py test`
