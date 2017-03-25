## ANK - Python Microservices ##


### Overview: ###
 Python Microservices Streaming, REST-API and Schedule task using queue message(rabbitMQ, zeromq, kafka)
 Each processor is a chain, put it together to make a pipeline.
 
 
### Support chain model:
* 1 - 1:
    ```
    processor - processor
    ```
* 1 - n:
    ```
             /  processor
    processor - processor
             \  processor
    ```
* n - 1:
    ```
    processor \
    processor - processor # get message at the first processor only
    processor /
    ```
* join message:
    ```
    message \
    message - [message, message, message]
    message /
    ```
* split message:
    ```
                                / message
    [message, message, message] - message
                                \ message
    ```
    

### Requirements: ###
* Python 2.x
* Python 3.x


### How to use: ###
* **Install:**
    * From github:
        - clone this project: `git clone git@github.com:sunary/ank.git`
        - install: `python setup.py install`
    * From pypi:
        - `pip install ank`
        
* **Create new Service:**
    ```shell
    $ ank -c TestService`
    $ cd TestService
    ```
    then continue using below commands

* **Edit app (processor.py):**
    * *Example:*
    ```python
    from base_apps.pipe_app import PipeApp

    class ExampleApp(PipeApp):
    
        def start(self):
            for i in range(100):
                self.chain_process(i)
    
        def process(self, message=None):
            '''
            Args:
                message: {'content': (*) 'content of message',
                          'flags': (list|tuple) 'define next process will be use'}
                              raise TypeError if you don't declare this in return of before braching-processor
                              if 'flags' == [True, True]: process both in next braching-processors
                              if 'flags' == [True, False]: process 1st processor in next braching-processors
                              if 'flags' == [False, True]: process 1st processor in next braching-processors
                              if 'flags' == [False, False]: stop chain
                          is None: stop chain
            '''
            return message['content'] + 1
    ```
    
* **Edit services and chains (services.yml):**
    * *Syntax:*
    ```yaml
    services:
      Object1:
        - class: module.name.ClassName
        - arguments: [$Object, %variable%] 
      
      AnkChain2:
        - class: apps.module_name.BuildinApps
        - arguments: ~
        
    chains:
      - Object1
      - AnkChain2
    ```
    * *Example:*
    ```yaml
    services:
      StartApp:
        class: processor.StartApp
        arguments: [$Mongodb, $Redis, '%batch_size%']
    
      Mongodb:
        class: utilities.my_mongo.Mongodb
        arguments: ['%mongo_db%', '%mongo_col%', '%mongo_host%', '%mongo_port%']
    
      Redis:
        class: redis.client.StrictRedis
        arguments: ['%redis_host%', '%redis_port%']
    
      OtherApp:
        class: processor.OtherApp
        arguments: ~
    
      LogApp:
        class: apps.log_app.LogApp
        arguments: ~
    
    chains:
      - StartApp
      - LogApp
      - OtherApp
      - [OddApp, EvenApp] # will be processed depend on key `flags`
      - OtherApp
    ```
    ANK will read top-down `chains`, find correspond `services` and get parameters from `settings.yml`.
    
* **Generate and edit setting (settings.yml):**
     ```shell
     $ ank -s
     ```
    * *Example:*
    ```yaml
    parameters:
      mongo_host: localhost
      mongo_port: 27017
      mongo_db: crawl_db
      mongo_col: twitter
      
      redis_host: localhost
      redis_port: 6379
      
      queue_uri: 'amqp://admin:admin@localhost:5672/'
      exchange_name: InputExchange
      routing_key: ExchangeToQueue
      
      batch_size: 100
    ```
    Help you create `settings` template file. Just rename from `_settings.yml` to `settings.yml` and fill in values.
    
* **Build Service (create docker image):**

    ```shell
    $ ank -b
    $ docker run --entrypoint /bin/sh docker_image_id
    ```
    
* **Generate processor (_processor.py):**
    
    ```shell
    $ ank -p
    ```
* **Edit and test Service (test_service.py):**

    ```shell
    $ ank -t -f test-settings.yml
    ```
* **Run Service:**

    ```shell
    $ ank -r
    ```
    
### Base Apps: ###
* **PipeApp:** Pipeline App.
* **APIApp:** REST-API inteface using flask.
* **ScheduleApp:** Using crontab-time format to set schedule.


### Build in Apps: ###
* **LogApp:** Log every messages.
* **JoinApp:** Join messages into one.
* **SplitApp:** Split message.
* **---Consumer:** Get message from queue.
* **---Producer:** Push message to queue.
