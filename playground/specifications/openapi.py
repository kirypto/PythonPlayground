from json import loads
from pathlib import Path
from typing import Dict, Set, Union

from openapi3 import OpenAPI
from openapi3.paths import Operation
from openapi3.schemas import Schema

JSONObject = Union[dict, str, int, list]


def construct_json_obj_from_schema(schema: Schema) -> JSONObject:
    if schema.example is not None:
        curr: JSONObject = schema.example
    elif schema.type == "string":
        curr: JSONObject = "string"
    elif schema.type == "integer":
        curr: JSONObject = 0
    elif schema.type == "boolean":
        curr: JSONObject = False
    elif schema.type == "object":
        curr: JSONObject = {}
        for prop_name, prop_schema in schema.properties.items():
            curr[prop_name] = construct_json_obj_from_schema(prop_schema)
    elif schema.type == "array":
        curr: JSONObject = [construct_json_obj_from_schema(schema.items)]
    elif len(schema.properties) > 0:
        curr: JSONObject = {}
        for prop_name, prop_schema in schema.properties.items():
            curr[prop_name] = construct_json_obj_from_schema(prop_schema)
    else:
        raise NotImplementedError(f"Unsupported schema type {schema.type}")
    return curr


class APISpecification(OpenAPI):
    def get_resources(self) -> Dict[str, Set[str]]:
        return {
            route_url: {
                method
                for method in ["get", "put", "post", "patch", "delete", "trace", "head", "options"]
                if hasattr(path_obj, method) and getattr(path_obj, method) is not None
            }
            for route_url, path_obj in self.paths.items()
        }

    def get_resource_request_body_examples(self, route: str, method: str) -> Dict[str, JSONObject]:
        resource_op: Operation = getattr(self.paths.get(route), method)
        if resource_op.requestBody is None:
            return {}
        examples: Dict[str, JSONObject] = {}
        for content_type, content_media in resource_op.requestBody.content.items():
            examples[content_type] = construct_json_obj_from_schema(content_media.schema)
        return examples


def _test():
    api_spec_text = Path(__file__).parent.joinpath("sample_openapi_v3.0.1.json").read_text()
    api_spec_json = loads(api_spec_text)

    api_specification = APISpecification(api_spec_json)
    routes = api_specification.get_resources()
    print(routes)
    for route, methods in routes.items():
        for method in methods:
            print(f"Resource {method} {route}")
            request_body_examples = api_specification.get_resource_request_body_examples(route, method)
            if request_body_examples:
                print(f" - Supported request bodies:")
                for content_type, example_body in request_body_examples.items():
                    print(f"   - {content_type}: {example_body}")


if __name__ == "__main__":
    _test()
