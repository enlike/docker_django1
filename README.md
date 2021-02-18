# Docker django

Simple Django project to start developing quickly

Stack: `Django, DRF, swagger, celery, celery-beat, rabbitmq, redis, PostgreSQL, pgbouncer`

## Start project

1. Install Docker
2. Execute this in project diretory
`docker-compose -f docker-compose-local.yml build && docker-compose -f docker-compose-local.yml up -d`
3. Add python interpreters *docker_django1\celery_dd\celery_scheduler_dd* services from **docker-compose-local.yml** 
4. Add these interpreters from 3 point to Run\Debug configurations for each of the services
5. Run and enjoy! :')
