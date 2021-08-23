
# APIs
POST api/v1/domain-request

GET api/v1/domain-request?period=<last_time_in_milis>

Setup an run:

    Localy on django dev server:
        1. Use python 3.8 or above, recommended to use virtual env.
        2. pip install -r requirements.txt
        4. python manage.py runserver 0.0.0.0:80
    
    Using docker-compose (django and nginx):
        1. docker-compose up -d --buld
    
    Using docker:
        1. docker build . -t exercise
        2. docker run --rm -d -p 80:8000 exercise python manage.py runserver 0.0.0.0:8000
  
### Use server
**add request**

curl -X POST <host>api/v1/domain-request -H "Content-type: application/json" -d '{"timestamp": 1608102631, "A": 3, "B": 4}'
    
**get top 10 domains last minute**
    
curl -X GET <host>api/v1/domain-request?period=60000
    

