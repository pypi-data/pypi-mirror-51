# Worker

Libreria la implementacion de workes basados en kafka y Nats.


### Ejemplo

```python
from Workerpy import Manager, Worker, Options

@Manager.Define(
    Options(
        'DemoWorker', # Nombre del worker
        'gitlab_push', # Topico/evento que escucha
        ['broker:123'] # Kafka/Nats Hosts
    )
)
class demo(Worker):
    def process(self, data):
        print(data)
```

> Los workes solo escuchan, no tienen posibilidad de responder