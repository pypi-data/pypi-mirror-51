# mbq.apitools

`mbq.apitools` is a python library for writing endpoints in Django. It provides a view decorator and view class that allow for strict typing of incoming query parameters and payloads, as well as consistent response shapes and status codes on the way out.

Some nice things about `mbq.apitools`:
* All fields specified in a param or payload schema are required by default, and can be marked as optional by providing a `default=` argument to the field class. The framework will automatically return a 400 response for all requests which do not conform to the specified schema. Details for each nonconforming field will be included in the response.
* The parsed parameters and payloads end up as rich types on the request. If a field is marked as `fields.DateTime`, then it will be on `request.payload` as a `datetime` object.
* Pagination is handled entirely by the framework. Simply include `paginated=True` when you define the view, return a `PaginatedResponse`, and voila!
* All success responses have a 200 status code.
* All list and paginated responses contain the list of resources under the key `"objects"`.
* All error responses have the same shape (an `"error_code"` and `"detail"` key).

## Example

```python
from mbq.api_tools import fields, responses
from mbq.api_tools.views import View, view

@view(
    "GET",
    permissions=[SomeDRFPermissionClass],
    params={
        "product_ids": fields.Int(default=None, many=True),
        "zipcode": fields.String(),
    }
)
def get_categories(request):
    categories = Category.objects.filter(zipcode=request.params.zipcode)

    if request.product_ids:
        categories = categories.filter(product_id__in=request.params.product_ids)

    categories = CategorySerializer(categories, many=True).data

    return responses.ListResponse(categories)


class OrdersView(View):

    @view.method("POST", payload={"company_id": fields.Int()})
    def create_order(self, request):
        order = create_order(request.payload.company_id)
        return responses.DetailResponse(OrderSerializer(order).data))

    @view.method("GET", permissions=[SomeDRFPermission], paginated=True)
    def get_orders(self, request):
        orders = Order.objects.all()
        return responses.PaginatedResponse(orders, OrderSerializer, request)
```
## Views

### @view

Use the `@view` decorator for all function based views. It accepts the following arguments:
* `http_method_name`
	* GET, POST, PATCH, PUT, DELETE
	* Defaults to GET
* `permissions`
	* A list of DRF permission classes _or_ functions that take in a request object and return `True` if authorized, `False` if unauthorized.
* `params`
	* Schema for validating incoming query parameters. The query parameters will be available at `request.params`.
* `payload`
	* Schema for validating incoming payloads. The payload will be available at `request.payload`.
* `paginated`
	* Boolean indicating if the response will be paginated or not. Defaults to `False`.
* `page_size`
	* Integer specifying the page size for a paginated response. This should only be used to override the default page size.
* `on_unknown_field`
	* `"raise"` or `"exclude"`. By default all endpoints will 400 if they receive an unknown query parameter or payload. This argument allows you to override the default behavior on a per view basis.

### View

Use the `View` class when you need to support multiple HTTP verbs for the same URL pattern.
The class exposes an `as_view()` method to use in `urls.py`.

All view methods on the class need to be marked with `@view.method(...)`, which supports the exact same interface as `@view`. (Note that unlike Django and DRF, since the verb is specified in the decorator you can name the view methods whatever you want.)

## Responses

Status codes are predefined by the different response classes. Status codes will _never_ be specified in a view.

### Success Responses

All success responses return a 200 status code.

#### `DetailResponse`

```python
responses.DetailResponse({"foo": "bar", "age": 10})
```
will generate:
```json
{"foo": "bar", "age": 10}
```

#### `ListResponse`
`ListResponse` accepts any iterable of JSON serializable python objects and will nest them under an `"objects"` key in the response.
```python
responses.ListResponse([{"foo": "bar"}])
```
will generate:
```json
{"objects": [{"foo": "bar"}]}
```

#### `PaginatedResponse`
`PaginatedResponse` accepts a `QuerySet`, a serializer, and a request. It will return a properly paginated response (according to the pagination params on the request) with the data under `"objects"` and a `"pagination"` key containing the pagination information.
```python
responses.PaginatedResponse(some_queryset, SomeDRFSerializer, request)
```
will generate:
```
{
    "objects": [{id: 1}, {id: 2}, {id: 3}, ... ],
    "pagination": {
        "page": 1,
        "page_size": 20,
        "num_pages": 5,
        "total_objects": 89,
        "next_page": "/api/v1/orders?page=2&page_size=20",
        "previous_page": null
    }
}
```
Alternatively, instead of a DRF Serializer class, you can pass in a function that takes in a list of objects and returns a list of serialized objects,
```python
responses.PaginatedResponse(
    some_queryset,
    lambda objs: [obj.to_dict() for obj in objs],
    request,
)
```
See the `Pagination` section for more details.

### Error Responses

All error responses will have the following shape:
```json
{"error_code": "some_unique_error_string", "detail": "More details about the error..."}
```
Some allow the `error_code` and `detail` to be specified, while others have them hard-coded.

#### `ClientErrorResponse`
* 400
* To be used when the client made an error it could have avoided.
* `error_code` and `detail` must be specified.
```python
responses.ClientErrorResponse("quote_state_error", "Cannot approve an already approved quote")
```

#### `UnauthenticatedResponse`
* 401
* `error_code`
  * `"unauthenticated"`
* `detail`
  * `"Authentication credentials were not provided"`

#### `UnauthorizedResponse`
* 403
* `error_code`
	* `"unauthorized"`
* `detail`
	* `"Unauthorized to access this resource"`

#### `NotFoundResponse`
* 404
* `error_code`
	* `"not_found"`
* `detail`
	* `"Resource not found"`

#### `ServerValidationErrorResponse`
* 422
* To be used when a validation error occurs that could only be detected by the server.
* `error_code` and `detail` must be specified.
 ```python
responses.ClientErrorResponse("email_already_taken", "The email you have provided is already in use")
```

#### `TooManyRequestsResponse`
* 429
* `error_code`
    * `"too_many_requests"`
```python
responses.TooManyRequestsResponse(detail="Too many requests for template")
```

#### `ServerErrorResponse`
* 500
* `error_code`
  * `"server_error"`
* `detail`
  * `"An unexpected error occurred"`

## Exceptions

### ValidationError
Use sparingly. If raised, the framework will catch it and return generate a `ClientErrorResponse`, with `"validation_error"` as the `error_code` and the error message as `detail`. However, in most cases you should just catch your own errors and return `ClientErrorResponse`.

### ImmediateResponseError
This exception takes in a response instance and, when raised, the framework will catch it and return the response it was instantiated with. This is useful when you have some shared function between two view functions and want to quickly bail in the shared function.
```python
class SomeObjView(View):
    def _get_some_obj(self, id):
        try:
            return SomeObj.objects.get(id=id)
        except:
            raise exceptions.ImmediateResponseError(responses.NotFoundResponse())

    @view.method("GET")
    def get_some_obj(request, id=None):
        obj = self._get_some_obj(id)
        ...

    @view.method("PATCH")
    def patch_some_obj(request, id=None):
        obj = self._get_some_obj(id)
        ...
```
## Schemas & Fields

Schemas and Fields use the Marshmallow library under the hood.

All schema fields support the following arguments:
* `default`
	* All fields in a schema are required by default. Use the `default` argument to both mark a field as optional and specify the default value to use if the field is not received.
	* If you would like the field to be left out entirely of the parsed params/payload, you can do `default=fields.OMIT`
*  `allow_none`
	* Defaults to `False`. Pass in `True` if you would like to accept `None` (`null`) as a passed in value.
* `validate`
	* Function that takes in the value and returns `True` or `False` appropriately.
* `transform`
	* Function that takes in the value and returns a value of the same type. This will run _before_ validation.
* `many`
	* Defaults to `False`. Pass in `True` if multiple values are allowed for the field. `many=True` will result in a list of values on the parsed params/payload.
	* For query parameters, this will support both comma separated values under a single arg (`?order_ids=1,2`) and multiple instances of the arg `(?order_ids=1&order_ids=2)`.
	* For payloads, a list of values is expected.
	* When used with `validate` and/or `transform`, these functions will be applied to each individual value.
* `param_name`
	* Use sparingly. It's to be used if the incoming query parameter will have a different name than the field name in the schema. For example, if the incoming query parameter will be specified as `?state=foo`, but you would like it to be `order_state` under `request.params`, you would do: `{"order_state": fields.String(param_name="state")}`

The available fields and their custom arguments are:
* `Bool`
* `DateTime`
* `Date`
* `Time`
* `Int`
	* `min_val`
	* `max_val`
* `String`
	* `min_length`
	* `max_length`
	* `allow_empty`
		* Defaults to `False`. If you would like to accept empty strings as valid values passed in, do `allow_empty=True`.
* `Enum`
	* `choices`
		* List of acceptable string values
* `UUID`
* `Float`
* `Decimal`
	* `max_digits`
    * `min_val`
    * `max_val`
* `Email`
* `Dict`
	* Use sparingly. Allows for any arbitrary dictionary to be passed in.

### Nested schemas

To nest a schema, do:
```python
@view(payload={
    "id": fields.Int(),
    "nested_object": fields.Nested({
        "name": fields.String()
    })
})
```
`Nested` fields accept all of the same arguments as the other fields.

### What about PATCH?

If you would like to support traditional PATCH behavior (where the client only sends down the fields to be updated), and need to know which fields were sent down or not, then doing something like `default=None` is not going to work for you. Normally, a field is either required, or has a default value and will appear on the parsed data with the default value if it was not sent down. Luckily, you can pass `default=fields.OMIT` to the field and it will be left out of the parsed data if it wasn't sent down. Here's an example:
```python
@view(
    "PATCH",
    payload={
       "first_name": fields.String(default=fields.OMIT),
        "last_name": fields.String(default=fields.OMIT)
    }
)
def update_person(request, id=None):
    person = Person.objects.get(id=id)

    data = request.payload.as_dict()

    if "first_name" in data:
        person.first_name = data["first_name"]
    if "last_name" in data:
        person.last_name = data["last_name"]

    person.save()

    return responses.DetailResponse()

```

## Pagination

The pagination mechanics are fully managed by the framework. All you have to do is specify `paginated=True` in the decorator, and return a `PaginatedResponse` object.

The expected query parameters when `paginated=True` are `page` and `page_size`.

`page` obviously defaults to `1`, and `page_size` defaults to `20`, but the client is more than welcome to send down a different value for `page_size`.

You can globally override the default `page_size` via the `API_TOOLS["DEFAULT_PAGE_SIZE"]` setting. You can override a particular view's default page size via the `page_size` argument to the decorator.

The pagination data returned in the response under the `pagination` key looks like:
```json
{
    "page": 1,
    "page_size": 20,
    "num_pages": 5,
    "total_objects": 89,
    "next_page": "/api/v1/orders?page=2&page_size=20",
    "previous_page": null
}
```
An empty page will be returned if the first page is requested and there is no data. Otherwise, if a non-existent page is requested, a 400 response will be returned.

## Requests

If `params` or `payload` is specified in the decorator, then the parsed query parameters will be at `request.params` or `request.payload`. This will be an immutable object. If you would like it in the form of a dictionary, you can do `request.params.as_dict()`.

## Permissions

Permissions are required. A non-empty list must be passed into the decorator. If you would like to write an unauthorized endpoint, you can do:
```python
from mbq.api_tools import permissions

@view(permissions=[permissions.NoAuthorization])
def my_view(request):
    pass
````

## Settings
The default settings are:
```python
API_TOOLS = {
    "DEFAULT_PAGE_SIZE": 20,
    "UNKNOWN_PAYLOAD_FIELDS": "raise",
    "UNKNOWN_PARAM_FIELDS": "raise",
}
```
Override as you see fit.
