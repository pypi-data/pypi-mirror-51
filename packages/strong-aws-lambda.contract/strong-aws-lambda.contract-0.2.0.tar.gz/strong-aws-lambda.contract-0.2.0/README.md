# Strong AWS Lambda

AWS lambdas are a very important feature from AWS platform, due to the intense use of it by the clients and also internally in order to enable other features.
Due to the intensive usage of it, I'd like to make its surrounds a bit more comfortable to develop on. 
As a developer with a big static programming language background, I created this module to bring the advantages of 
a static type language to the python lambda world  (especially custom resources) + automate some repetitive code we always create while
using lambdas, like parsing the event input information, guarantee the correct result, etc.


## Usage
The solution is based in some new decorators, which brings extra features for the lambda handlers.
As you might know, the first params for a lambda handler or a custom resource handler is and object event. 
Which in lambda can be anything but for custom resource is for sure a dictionary with values.


This library convert the event to an object of a given contract you defined and call the function using the new object.
Before that it execute all the static typing and consistency with between the given params and the expected params.


The contract must to be a `dataclass` where the name of the fields will be the name of the keys you want to exist in
the call to your lambda/custom resource. In case the conversion fails a `ValueError` exception will raise informing
which fields were missing in the `event` params. The message will raise as:

`ValueError: Keys ['X', 'Y', 'Z'] not found in event`, where `X`, `Y` and `Z` are the fields which couldn't be found in 
the `event` param.

This also checks for the types you define. If in your contract you expect `field1` as `str` but the information is 
sent as `int` for example. The conversion will fail and raise the given exception:

`WrongTypeError: wrong type for field "X" - should be "str" instead of "int"`, where `X` will be the 

The conversions are use as engine the `dacite` project. So if you want to check more information, how the mapping 
from and dictionary to `dataclass` works and what are the possibilities. 
Check their project [here](https://github.com/konradhalas/dacite)   


### Lambdas
You just need to add the decorator `strong_aws_lambda` and set the param `contract_class` with your desired contract 
dataclass on your lambda handler.
Check the example below where we have the contract class `FooContract`. Keep in mind that your contract classes 
must to have the decorator `dataclass`.

```python
from dataclasses import dataclass
from typing import List
from aws_lambda_context import LambdaContext
from strong_aws_pkg import strong_aws_lambda


@dataclass
class FooContract:
    field1: str
    field2: int
    items: List[str]


@strong_aws_lambda(contract_class=FooContract)
def lambda_handler(event: FooContract, context: LambdaContext):
    print(f'The field is for sure in event object and its type is a str. The value is {event.field1}')
    print(f'The field is for sure in event object and its type is an int. The value is {event.field2}')
    print(f'And there are {len(event.items)} in the items object')
    [print(f'And the value of the item is {item}') for item in event.items]
    
# Just mocking a call the way AWS might to do to the function in order to check its behave.
if __name__ == "__main__":
    input = dict(field1='test1', field2=1, items=['value1', 'value2', 'value3'])
    lambda_handler(input, LambdaContext())

    invalid_input = dict(unknown_field='test1', unknown_field2=1, other_items=['value1', 'value2', 'value3'])
    lambda_handler(invalid_input, LambdaContext())
```

The console output for this code will be:
```text
The field is for sure in event object and its type is a str. The value is test1
The field is for sure in event object and its type is an int. The value is 1
And there are 3 objects in the items object
And the value of the item is value1
And the value of the item is value2
And the value of the item is value3
Keys ['field1', 'field2', 'items'] not found in event
```

### Custom Resources
Custom resources have a bit more complicated situation as they need to communicate back to AWS in order to give the 
information about the CloudFormation Stack its changing.
Here is where you have more gain using this library, as it will ensure that all the information needed will exist
in the in and out contract.

For example, even if you forget to add the `Status` in your return, this this library will wrap it into a understandable 
object where AWS can act accordingly without blocking the finalization of the action.

For this decorator you need to set to parameters:
1. `contract_class`: You need to pass your defined contract class which must to have the decorator `@dataclass(frozen=True)`, 
and inherit from `BaseResourceProperties`.
1. `handle_untreated_exceptions` (default value is `true`): Tell to the decorator function what to do to untreated exceptions. If it's `true` it will
wrap the exception message into a expected AWS format. If `false` it won't change the result and you will have problems to 
execute further iterations in stack this custom resource have been created.

The reason the `dataclass` decorator has its attribute `frozen` se to `true` is due to the fact we want to have 
immutability in our contract objects.  

Given the python code example:
```python
from dataclasses import dataclass
from typing import List

from aws_lambda_context import LambdaContext
from cfn_lambda_handler import Handler

from strong_aws_pkg import AwsRequestContract, BaseResourceProperties, BaseResultContract, StatusResult, \
    strong_aws_lambda_custom_resource

handler = Handler()


###########################
# Example of handler create
###########################

@dataclass(frozen=True)
class HandlerCreateContract(BaseResourceProperties):
    CustomParam1: str
    CustomParam2: List[int]


@dataclass(frozen=True)
class HandlerCreateResultContract(BaseResultContract):
    CustomParams1: str


@handler.create
@strong_aws_lambda_custom_resource(contract_class=HandlerCreateContract, handle_untreated_exceptions=True)
def handler_create(custom_params: HandlerCreateContract, context: LambdaContext,
                   aws_params: AwsRequestContract) -> HandlerCreateResultContract:
    print(custom_params)
    print(context)
    print(aws_params)
    return HandlerCreateResultContract(Status=StatusResult.Success, CustomParams1='Everything went fine :) Cheers!')


###########################
# Example of handler update
###########################

@dataclass(frozen=True)
class HandlerUpdateContract(BaseResourceProperties):
    Field1: str


@handler.update
@strong_aws_lambda_custom_resource(HandlerUpdateContract)
def handler_update(custom_params: HandlerUpdateContract, context: LambdaContext,
                   aws_params: AwsRequestContract) -> BaseResultContract:
    raise Exception('Unexpected error')


###########################
# Example of handler delete
###########################

@dataclass(frozen=True)
class HandlerDeleteContract(BaseResourceProperties):
    Reason: str


@handler.delete
@strong_aws_lambda_custom_resource(HandlerDeleteContract)
def handler_delete(event: HandlerDeleteContract, context: LambdaContext,
                   aws_params: AwsRequestContract) -> BaseResultContract:
    if event.Reason:
        print(f'Deleting stack because {event.Reason}')
    else:
        print(f'Deleting stack')

    return BaseResultContract(StatusResult.Success)


# Just mocking a call the way AWS might to do to the function in order to check its behave.
if __name__ == "__main__":
    print('-------  Calling handler_create')
    # Input example got from https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html
    aws_input_param = {
        "RequestType": "Create",
        "ResponseURL": "http://pre-signed-S3-url-for-response",
        "StackId": "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
        "RequestId": "unique id for this create request",
        "ResourceType": "Custom::TestResource",
        "LogicalResourceId": "MyTestResource",
        "ResourceProperties": {
            "CustomParam1": "Value",
            "CustomParam2": [1, 2, 3]
        }
    }
    result = handler_create(aws_input_param, LambdaContext())
    print(result)

    print('-------  Calling handler_update')
    aws_update_param = {
        "RequestType": "Update",
        "ResponseURL": "http://pre-signed-S3-url-for-response",
        "StackId": "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
        "RequestId": "unique id for this create request",
        "ResourceType": "Custom::TestResource",
        "LogicalResourceId": "MyTestResource",
        "ResourceProperties": {
            "Field1": "Value"
        }
    }
    result = handler_update(aws_update_param, LambdaContext())
    print(result)

    print('-------  Calling handler_delete')
    aws_delete_param = {
        "RequestType": "Delete",
        "ResponseURL": "http://pre-signed-S3-url-for-response",
        "StackId": "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
        "RequestId": "unique id for this create request",
        "ResourceType": "Custom::TestResource",
        "LogicalResourceId": "MyTestResource",
        "ResourceProperties": {
            "Reason": "All work done"
        }
    }
    result = handler_delete(aws_delete_param, LambdaContext())
    print(result)

```

You will get this output in your console:
```text
-------  Calling handler_create
HandlerCreateContract(CustomParam1='Value', CustomParam2=[1, 2, 3])
<aws_lambda_context.LambdaContext object at 0x107faec18>
AwsRequestContract(RequestType='Create', ResponseURL='http://pre-signed-S3-url-for-response', StackId='arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid', ResourceType='Custom::TestResource', LogicalResourceId='MyTestResource')
{"Status": "SUCCESS", "CustomParams1": "Everything went fine :) Cheers!"}
-------  Calling handler_update
{"Status": "FAILED", "Reason": "Unexpected error"}
-------  Calling handler_delete
Deleting stack because All work done
{"Status": "SUCCESS"}
```

As you my have noticed the `handler_update` was raising and not treating an exception. This is bad because AWS 
expects an answer in a specific way. A dictionary with at least a key `Status`, with value `FAILED` or `SUCCESS`. 
As in this case the `handle_untreated_exceptions` param was set to `true`, the result is a well formatted object:

 `{"Status": "FAILED", "Reason": "Unexpected error"}`

```python
@handler.update
@strong_aws_lambda_custom_resource(HandlerUpdateContract, handle_untreated_exceptions=False)
def handler_update(custom_params: HandlerUpdateContract, context: LambdaContext,
                   aws_params: AwsRequestContract) -> BaseResultContract:
    ...
    ...
    ...
```


## Further Reading
If you are not very familiar with the terms I mentioned above, I put some links together in order to bring more clarity 
to the topics. 
1. [Static vs Dynamic Typing](https://hackernoon.com/i-finally-understand-static-vs-dynamic-typing-and-you-will-too-ad0c2bd0acc7)
1. [The benefits of static typing without static typing in Python](https://pawelmhm.github.io/python/static/typing/type/annotations/2016/01/23/typing-python3.html
) 
1. [AWS Lambda](https://aws.amazon.com/lambda/)
1. [AWS Custom Resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html)
1. [typing Python — Support for type hints](https://docs.python.org/3/library/typing.html)
1. [Immutable objects](https://en.wikipedia.org/wiki/Immutable_object)
1. [Why Immutability Matters](https://pasztor.at/blog/why-immutability-matters)
