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
- unittest,
- Docker.

Thanks to this project, I acquired skills in using the Django framework and the DjangoRESTFramework. Among other things, I gained experience in creating a complex CRUD system and implementing effective validation and permission mechanisms. What's more, I acquired skills in managing user accounts, including login, registration and logout.

Another aspect was the creation of complete tests to verify the written code.

As for future improvements, I intend to improve account management by implementing features such as password reset. Another objective will be even higher security. What's more, I also plan to add a front-end to enable a clear way to use the application.

In addition, I intend to add a function to analyze training results, allowing users to determine their progress.

## How to Install the Project

1. Create a .env file. An example of a finished file is:  

   > DJANGO_SECRET_KEY=super-secret-key123  
   > DEBUG=1  
   > DJANGO_ALLOWED_HOST=127.0.0.1 localhost  
   > POSTGRES_DB=myworkoutplandb  
   > POSTGRES_USER=myworkoutplanuser  
   > POSTGRES_PASSWORD=secretpassword123

2. Run the following command to start the application:  
   `docker compose up`

3. The application will be available at: http://localhost:8000/

4. [Optional] Swagger documentation will be available at:  
    http://localhost:8000/api/schema/swagger-ui/

__To create a superuser you should:__

1. Get the ID of the web container by running the following command:  
   `docker ps`

2. Enter the web container by running the following command:  
   `docker exec -it {id of container} bash`

3. Database migration:  
   `python manage.py createsuperuser`

## How to run the Project

If you have installed the application in the correct way is enough:  
`docker compose up`

And the application will be available at: http://localhost:8000/

## How to run tests

1. Start the application using the commands in the previous sections.  
2. Get the ID of the web container by running the following command:  
   `docker ps`
3. Enter the web container by running the following command:  
   `docker exec -it {id of container} bash`
4. Run tests with the following command:  
   `python manage.py test`
   or  
   `coverage run manage.py test`