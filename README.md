## My workout plan

An application written in Python in Django to create professional training plans.
The Application is under development.
Backend will be priority. In the case of Frontend, it will be quite simple.

## Project Description

The project will be have some functionalities:

- Creating, editing, deleting trainins,
- Creating, editing, deleting plans,
- Adding training results to monitor progress,
- Possibility to search for exercises for specific muscle parts. Here will be insprition of site: https://musclewiki.com/.

The application will be used:

- Django,
- Django RESTFramework,
- HTML,CSS
- Others

## What is to do

- changing API - using Django REST Framework (include checking JSON web tokens and similar things to authentication)
- admin panel
- improvments of html and little css - grid, flexbox and so on
- login with using email
- adding avatars to users
- password reset

- connecting with a postgres database
- tests of application

- muscle wiki:
  -- CRUD with difference between admin and user
  Important: It is necessary to use django rest framework
  It will be two tables one w partial of muscle
  Second with exercises to this partial of muscle

Muscle:

- forearms,
- biceps,
- triceps,
- shoulders,
- chest,
- ABS,
- Back,
- glutes,
- quads,
- hamstrings,
- adductors, (przywodziciele)
- calves.

Exercise:

- name,
- muscle (possibility to add few),
- technique
