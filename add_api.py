#!/usr/bin/env python3
import argparse
import yaml
from contextlib import contextmanager
from pathlib import Path


def main(api_id: str, api_spec_url: str):
    api_dir_path = Path("./openapi") / api_id
    api_dir_path.mkdir()

    reference_page_path = api_dir_path / "reference.page.yaml"
    with edit_yaml(reference_page_path) as content:
        content["type"] = "reference-docs"
        content["definitionId"] = api_id
        content["settings"] = {"jsonSampleExpandLevel": "all"}

    with edit_yaml("./sidebars.yaml") as content:
        content["training"].append({"label": api_id, "page": str(reference_page_path)})

    with edit_yaml("./siteConfig.yaml") as content:
        content["oasDefinitions"][api_id] = api_spec_url


@contextmanager
def edit_yaml(path: str):
    file_path = Path(path)
    if file_path.exists():
        with file_path.open(mode="r") as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
    else:
        content = {}
    yield content
    with file_path.open(mode="w") as f:
        yaml.safe_dump(content, f)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add new api")
    parser.add_argument("api_id", type=str, help="Identifier of your api, no space")
    parser.add_argument("api_spec_url", type=str, help="URL of your API spec")
    args = parser.parse_args()
    main(api_id=args.api_id, api_spec_url=args.api_spec_url)
