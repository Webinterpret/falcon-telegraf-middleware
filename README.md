# falcon-telegraf-middleware

[![forthebadge](https://forthebadge.com/images/badges/built-with-resentment.svg)](https://forthebadge.com)

## What is this?

Package to ease gathering metrics from [Falcon](http://falcon.readthedocs.io/) APIs into InfluxDB via a Telegraf.
By use of middlewares this orthogonal functionality is added in a hassle-free way minimizing required work. Sane defaults make quickstart really quick 👍

## How?
Inject the middleware (or couple of them) when creating `Api` instance:

```python
telegraf_client = TelegrafClient('localhost', 8094)
app = falcon.API(
    middleware=[
        LogHits(telegraf_client),
        TimeRequests(),
    ]
)
```

Note that passing `telegraf_client` is totally optional.
Measurement names can be set when creating middleware, prefixed or autogenerated.

## Middlewares
### `LogHits`
Creates a metric named hits-path/to/endpoint with one fields called `hits` with value 1.
### `LogHitsContextAware`
Similar to `LogHits` but executes *after* `on-*` method was called and adds more context data. Because of this you can add custom tags.
Example:
```python
def on_get(self, request, response, some_path_variable):
    request.context['my_new_tag'] = 'this_tags_value'
    request.context['some_path_variable'] = some_path_variable  ## this is unnecessary - it's logged by middleware
    ...
```
It's metric name is the same as for `LogHits`.
Note that using this two middlewares in the sam API doesn't make any sense.
### `Timer`
Reports time in ms elapsed between registering response and registering request. Default metric prefix is `time-`.
Other things in processing pipeline can affect it's readings so take them with a grain of salt. 
## Deploy
First bump version in `setup.py` in master branch via merge request. Afterwards push a version tag and wait.

```bash
git tag `date +"%Y.%-m.%-d.1"`
git push --tags
```
