PyCTX for Django
================

**django-pyctx** is a context package to use data between function calls, use timers and log it.

For detailed documentation please visit [Wiki](https://github.com/molcay/django-pyctx/wiki).

Quick Start
-----------

1. Add **django_pyctx** to your ``INSTALLED_APPS``  setting like this:

   ```python
   INSTALLED_APPS = [
    #...,
    "django_pyctx",
   ]
   ```

2. Add **django_pyctx.middlewares.RequestCTXMiddleware** to your ``MIDDLEWARE`` setting like this:

   ```python
   MIDDLEWARE = [
     "django_pyctx.middlewares.RequestCTXMiddleware",
     # ...,
   ]
   ```

> Please add "django_pyctx.middlewares.RequestCTXMiddleware" to at the beginning of the MIDDLEWARE list.

3. Start the development server and enjoy :)

Sample Usage
------------

- You can reach `RequestContext` instance in **views** from `request`: `request.ctx`

- Example django function-based `view`:

    ```python
  from django.http import JsonResponse
  
  
  def run(request):
    y = 5
    with request.ctx.log.timeit('index_timer'):
        request.ctx.log.set_data('isEven', y % 2)
        request.ctx.log.set_data('y', y)
        request.ctx.log.start_timer('timer1')
        import time
        time.sleep(1)
        request.ctx.log.stop_timer('timer1')
        time.sleep(5)
        return JsonResponse({})
    ```

You can see the stdout. You are probably seeing something like this:

```json
{
  "type": "REQ",
  "ctxId": "28d30c66-6c00-405e-b3ac-e931097b6e50",
  "startTime": "2019-08-23 10:48:18.555994",
  "endTime": "2019-08-23 10:48:24.566458",
  "data": {
    "isEven": 1,
    "y": 5
  },
  "timers": {
    "ALL": 6.010477,
    "request": 6.010464,
    "index_timer": 6.008194,
    "timer1": 1.004116
  },
  "http": {}
}
```
> NOTE: this output formatted
