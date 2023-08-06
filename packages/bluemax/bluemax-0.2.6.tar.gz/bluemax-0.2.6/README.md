# bluemax

bluemax is a python rpc server using websockets.

The concept is that you can write python functions and
expose them in the `__all__` property of the module.

The complexity comes when you want to do more than
this. And that is what I am working on. The most
important pattern to me is being able to insert, update
and delete in the database and be able to broadcast
the changes to all users after the actor gets their
response. I call it broadcast_on_success.

        actor   crud    broadcast
          |       |         |
          |------>|         |
          |       |         |
          |<------|         |
          |       |-------->|
          |       |         |
          |<------|---------|
          |       |         |

  The errors from crud are local to the actor. The actor
  will receive identity on success and then like every
  other user hear about crud via broadcast.

  Using annotations allows clients to
  infer function. See the sample.add function.

For deployment of multiple servers see:

  http://www.tornadoweb.org/en/stable/guide/running.html#running-behind-a-load-balancer

To use:
```
pip install bluemax
```

To install:
```
python3.7 -m venv venv
. venv/bin/activate
pip install -e git+https://bitbucket.org/blueshed/bluemax.git#egg=bluemax
```

To run you can choose either with workers using redis or standalone.

To run standalone:
```
bluemax run.server -m bluemax.tests.foo
```

To run with redis:
```
pip install bluemax[redis]
docker run -p 6379:6379 -d redis:2.8
```

Then create a conf.yml file containing:
```
---
procedures: tests.foo
services: tests.foo.services
REDIS_URL: redis://localhost
```
Then run a worker in one terminal
and a server in the another.
```
bluemax run.worker -c conf.yml
```
and
```
bluemax run.services -c conf.yml
```
and
```
bluemax run.server -c conf.yml
```

Now go to http://localhost:8080 and add some numbers.

To build your own project try:
```
bluemax sidney olive
```
You can use any name for your module. It will create extension points for logs,
settings, urls and a base procedures modules. bluemax will look for your
procedures.__all__ in the module you pass in.
