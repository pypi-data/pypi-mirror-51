GD-rabbitMQ
---
**Right now this package is only for ```greendeck's``` internal use. This will help to publish and consume messages with your rabbitMQ**

![Greendeck](https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/gd_transparent_blue_bg.png)  ![RabbitMQ](https://greendeck-cdn.s3.ap-south-1.amazonaws.com/dumps/rabbitmq.png)
### Install from pip
https://pypi.org/project/greendeck-rabbitmq/

```pip install greendeck-rabbitmq```


### How to use ?
##### import the library
```python
import greendeck_rabbitmq
```

##### import ```RabbitMQ``` class
```python
from greendeck_rabbitmq import RabbitMQ
```

##### initialize ```RabbitMQ``` client connection
```python
from greendeck_rabbitmq import RabbitMQ

# declare variables
RMQ_HOST = <YOUR_RMQ_HOST>
RMQ_PORT = <YOUR_RMQ_PORT>
RMQ_VHOST = <YOUR_RMQ_VHOST>
username = <YOUR_USERNAME>
password = <YOUR_PASSWORD>

```Here default values are RMQ_PORT=5678, RMQ_VHOST='\', username=Null, password=Null```

rabbitmq_client = RabbitMQ(RMQ_HOST, RMQ_PORT, RMQ_VHOST, username, password)

```
Here default values of some arguments are 
* RMQ_PORT=5678
* RMQ_VHOST='\'
* username=Null
* password=Null


##### close ```RabbitMQ``` client connection
```python
rabbitmq_client.rabbitmq_close_connection()
```
##### check size of a rabbitmq queue
```python

queue = "test_library"
print(rabbitmq_client.size(queue))
```
##### check if a size of queue is empty or not
```python

queue = "test_library"

print(rabbitmq_client.is_empty(queue))
```

##### consume all messages of a queue
```python
queue = "test_library"
rabbitmq_client.rabbitmq_get_all(queue)

```

##### single message producer
```python
message = "hello world"
queue = "test_library"
routing_key = "test_library"
exchange = ''
delivery_mode = 2
mode = "single"

```default values are exchange = '', delivery_mode = 2, mode = "single" ```

```available modes are 'single' & 'multi' and in 'multi' mode it expects message as list of messages

rabbitmq_client.rabbitmq_publisher(message, queue, routing_key, exchange, delivery_mode, mode)
rabbitmq_client.rabbitmq_close_connection()
```

##### multi messages producer
```python
message = ["hello world"] * 100  #list of messages
queue = "test_library"
routing_key = "test_library"
exchange = ''
delivery_mode = 2
mode = "multi"

rabbitmq_client.rabbitmq_publisher(message, queue, routing_key, exchange, delivery_mode, mode)
rabbitmq_client.rabbitmq_close_connection()
```

##### messages consumer
```python
queue = "test_library"
size = 1 # mention number of required messages

```here default parameter is size =1```

results = rabbitmq_client.rabbitmq_consumer(queue, size)
print("number of messages", len(results))
rabbitmq_consumer.rabbitmq_close_connection()

```

---
How to build your pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

Update your package
* ```python setup.py sdist```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5
* https://packaging.python.org/tutorials/packaging-projects/RabbitMQ

# Thank You