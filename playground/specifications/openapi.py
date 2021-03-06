from collections import defaultdict
from json import loads
from pathlib import Path
from typing import Dict, Set, Union, Optional

from openapi3 import OpenAPI
from openapi3.paths import Operation
from openapi3.schemas import Schema

JSONObject = Union[dict, str, int, list]


def construct_json_obj_from_schema(schema: Schema) -> JSONObject:
    def object_from_properties(properties: Optional[Dict[str, Schema]]):
        if not properties:
            return {}
        return {
            prop_name_: construct_json_obj_from_schema(prop_schema_)
            for prop_name_, prop_schema_ in properties.items()
        }

    if schema.example is not None:
        curr: JSONObject = schema.example
    elif schema.type == "string":
        curr: JSONObject = "string"
    elif schema.type == "integer":
        curr: JSONObject = 0
    elif schema.type == "boolean":
        curr: JSONObject = False
    elif schema.type == "array":
        curr: JSONObject = [construct_json_obj_from_schema(schema.items)]
    elif schema.type == "object" or len(schema.properties) > 0:
        return object_from_properties(schema.properties)
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

    def get_resource_response_body_examples(self, route: str, method: str) -> Dict[str, Dict[str, JSONObject]]:
        resource_op: Operation = getattr(self.paths.get(route), method)
        examples: Dict[str, Dict[str, JSONObject]] = defaultdict(dict)
        for status_code, media_for_status_code in resource_op.responses.items():
            if not media_for_status_code.content:
                examples[status_code]["*/*"] = {}
            else:
                for content_type, content_media in media_for_status_code.content.items():
                    examples[status_code][content_type] = construct_json_obj_from_schema(content_media.schema)
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
            response_body_examples = api_specification.get_resource_response_body_examples(route, method)
            if response_body_examples:
                print(f" - Possible response bodies:")
                for status_code, examples_for_status_code in response_body_examples.items():
                    print(f"   - {status_code}:")
                    for content_type, example_body in examples_for_status_code.items():
                        print(f"     - {content_type}: {example_body}")


if __name__ == "__main__":
    _test()
