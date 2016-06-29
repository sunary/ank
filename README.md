## ANK - Python Microservices ##


### Overview: ###
 Python microservices for Queue(RabbitMQ, Kafka), Streaming, REST-API and Schedule task.


### Requirements: ###
* Python 2.7


### How to use: ###
* **Create virtualenv `worker` and install ANK:**

    ```shell
    $ virtualenv worker
    $ source worker/bin/activate
    $ pip install ank
    $ # or pip install -e git+ssh://git@github.com/sunary/ank.git#egg=ank
    ```
    Your App will run on this virtualenv `worker`.
* **Create chains (E.g: `WorkerClass`, `OtherWorker`), register it with other ANK's `chains` (E.g `LogHandle`) into `services.yml`:**
    * *Example:*
    ```python
    from apps._app import App

    class ExampleApp(App):
    
        def run(self, process=None):
            '''
            Implement this if your App start by this chain
            Arguments:
                process: process method, was assign into self._process
                
            '''
            super(TestApp, self).run(process)
    
            for i in range(100):
                self._process(i)
    
        def process(self, message=None):
            # after processed, message will be return for next chain
            message += 1
            return message
    ```
* **Create services and chains:**
    * *Syntax:*
    ```yaml
    services:
      Object1:
        - class: module.name.ClassName
        - arguments: [$Object, %variable%] 
      
      AnkChain2:
        - class: chains.module_name.Chain
        - arguments: ~
        
    chains:
      - Object1
      - AnkChain2
    ```
    * *Example:*
    ```yaml
    services:
      WorkerClass:
        class: processor.DemoApp
        arguments: [$Mongodb, $Redis, '%batch_size%']
    
      Mongodb:
        class: utils.my_mongo.Mongodb
        arguments: ['%mongo_db%', '%mongo_col%', '%mongo_host%', '%mongo_port%']
    
      Redis:
        class: redis.client.StrictRedis
        arguments: ['%redis_host%', '%redis_port%']
    
      OtherWorker:
        class: processor.OtherApp
        arguments: ~
    
      LogHandle:
        class: chains.log_handle.LogHandle
        arguments: ~
    
    chains:
      - WorkerClass
      - LogHandle
      - OtherWorker
    ```
    ANK will read top-down `chains`, find correspond `services` and get parameters from `settings.yml`.
* **Generate setting:**
     ```shell
     $ gen_setting
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
      
      queue_uri: ['amqp://admin:admin@localhost:15672/']
      queue_name: InputQueue
      
      batch_size: 100
    ```
    Help you create `settings` template file. Just rename from `_settings.yml` to `settings.yml` and fill in values.
* **Install requirements of App into virtualenv `worker`:**

    ```shell
    $ pip install -r requirements.txt
    ```
* **Generate processor:**
    
    ```shell
    $ gen_processor
    ```
* **Run (Directly, using generated `_processor.py`):**

    ```shell
    $ python _processor.py
    ```
* **Run (Dependency Injection):**

    ```shell
    $ PYTHONPATH=$(pwd) start_app
    ```
    
### Apps: ###
* **App:** Normal App.
* **API App:** REST-API using flask.
* **Schedule App:** Using crontab-time format to set schedule.


### Chains: ###
* **LogHandle:** Log every messages.
* **JoinProcessor:** Join messages into one.
* **SplitProcessor:** Split message.
* **GetMessage:** Get messages from queue.
* **PostMessage:** Post message to exchange.