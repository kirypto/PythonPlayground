from json import loads
from pathlib import Path
from typing import Dict, Set

from openapi3 import OpenAPI


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
    api_spec_text = Path(__file__).parent.joinpath("sample_openapi_v3.0.1.json").read_text()
    api_spec_json = loads(api_spec_text)

    api_specification = APISpecification(api_spec_json)
    print(api_specification.get_routes())


if __name__ == "__main__":
    _test()
