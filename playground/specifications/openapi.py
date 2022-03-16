from typing import Dict, Set

from openapi3 import OpenAPI
from requests import get


class APISpecification(OpenAPI):
    def get_routes(self) -> Dict[str, Set[str]]:
        return {
            route_url: {
                method
                for method in ["get", "put", "post", "patch", "delete", "trace", "head", "options"]
                if hasattr(path_obj, method) and getattr(path_obj, method) is not None
            }
            for route_url, path_obj in self.paths.items()
        }


def _test():
    api_spec_json = get("https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore-expanded.json").json()

    api_specification = APISpecification(api_spec_json)
    print(api_specification.get_routes())


if __name__ == "__main__":
    _test()
