#sidanwebframework

##this framework can be used to develop python based web applications

```
from sidanwebframework import Server, Response, route, Render
```

```
@route('/index')
def index(request):
    return Response('Hello world')
```

```
@route('/home')
def home(request):
    return Render('home.html')
```

```
app = Server()
app.serve()
```
