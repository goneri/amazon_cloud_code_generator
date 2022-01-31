#!/usr/bin/env python3

import argparse
from typing import DefaultDict
import json
import os
import pathlib
import pkg_resources
from pbr.version import VersionInfo
import yaml

import re

def _camel_to_snake(name, reversible=False):
    # From https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/common/dict_transformations.py
    def prepend_underscore_and_lower(m):
        return '_' + m.group(0).lower()

    if reversible:
        upper_pattern = r'[A-Z]'
    else:
        # Cope with pluralized abbreviations such as TargetGroupARNs
        # that would otherwise be rendered target_group_ar_ns
        upper_pattern = r'[A-Z]{3,}s$'

    s1 = re.sub(upper_pattern, prepend_underscore_and_lower, name)
    # Handle when there was nothing before the plural_pattern
    if s1.startswith("_") and not name.startswith("_"):
        s1 = s1[1:]
    if reversible:
        return s1

    # Remainder of solution seems to be https://stackoverflow.com/a/1176023
    first_cap_pattern = r'(.)([A-Z][a-z]+)'
    all_cap_pattern = r'([a-z0-9])([A-Z]+)'
    s2 = re.sub(first_cap_pattern, r'\1_\2', s1)
    return re.sub(all_cap_pattern, r'\1_\2', s2).lower()

def main():
    parser = argparse.ArgumentParser(description="Build the amazon.cloud modules.")
    parser.add_argument(
        "--target-dir",
        dest="target_dir",
        type=pathlib.Path,
        default=pathlib.Path("amazon.cloud"),
        help="location of the target repository (default: ./amazon.cloud)",
    )
    parser.add_argument(
        "--next-version", type=str, default="TODO", help="the next major version",
    )
    args = parser.parse_args()

    module_list = []
    for json_file in ["aws-s3-bucket.json"]:
        print("Generating modules from {}".format(json_file))
        raw_content = pkg_resources.resource_string(
            "amazon_cloud_code_generator", f"aws_cloudformation_schemas/{json_file}"
        )
        print(raw_content)
        # swagger_file = SwaggerFile(raw_content)
        # resources = swagger_file.init_resources(swagger_file.paths.values())

        # for resource in resources.values():
        #     if "list" in resource.operations:
        #         module = AnsibleInfoListOnlyModule(
        #             resource, definitions=swagger_file.definitions
        #         )
        #         if module.is_trusted() and len(module.default_operationIds) > 0:
        #             module.renderer(
        #                 target_dir=args.target_dir, next_version=args.next_version
        #             )
        #             module_list.append(module.name)
        #     elif "get" in resource.operations:
        #         module = AnsibleInfoNoListModule(
        #             resource, definitions=swagger_file.definitions
        #         )
        #         if module.is_trusted() and len(module.default_operationIds) > 0:
        #             module.renderer(
        #                 target_dir=args.target_dir, next_version=args.next_version
        #             )
        #             module_list.append(module.name)

        #     module = AnsibleModule(resource, definitions=swagger_file.definitions)

        #     if module.is_trusted() and len(module.default_operationIds) > 0:
        #         module.renderer(
        #             target_dir=args.target_dir, next_version=args.next_version
        #         )
        #         module_list.append(module.name)

    files = [f"plugins/modules/{module}.py" for module in module_list]
    files += ["plugins/module_utils/core.py"]
    ignore_dir = args.target_dir / "tests" / "sanity"
    ignore_dir.mkdir(parents=True, exist_ok=True)
    # ignore_content = (
    #     "plugins/modules/vcenter_vm_guest_customization.py pep8!skip\n"  # E501: line too long (189 > 160 characters)
    #     "plugins/modules/appliance_infraprofile_configs.py pep8!skip\n"  # E501: line too long (302 > 160 characters)
    # )

    for version in ["2.9", "2.10", "2.11", "2.12", "2.13"]:
        skip_list = [
            "compile-2.7!skip",  # Py3.6+
            "compile-3.5!skip",  # Py3.6+
            "import-2.7!skip",  # Py3.6+
            "import-3.5!skip",  # Py3.6+
            "future-import-boilerplate!skip",  # Py2 only
            "metaclass-boilerplate!skip",  # Py2 only
        ]
        # No py26 tests with 2.13 and greater
        if version in ["2.9", "2.10", "2.11", "2.12"]:
            skip_list += [
                "compile-2.6!skip",  # Py3.6+
                "import-2.6!skip",  # Py3.6+
            ]
        if version in ["2.9", "2.10", "2.11"]:
            skip_list += [
                "validate-modules:missing-if-name-main",
                "validate-modules:missing-main-call",  # there is an async main()
            ]
        elif version == "2.12":
            # https://docs.python.org/3.10/library/asyncio-eventloop.html#asyncio.get_event_loop
            # with py3.10, get_event_loop() raises a deprecation warning. We will switch to asyncio.run()
            # when we will drop py3.6 support.
            skip_list += [
                "import-3.10!skip",
            ]

        # per_version_ignore_content = ignore_content
        for f in files:
            for test in skip_list:
                # Sanity test 'validate-modules' does not test path 'plugins/module_utils/vmware_rest.py'
                if version in ["2.9", "2.10", "2.11"]:
                    if f == "plugins/module_utils/vmware_rest.py":
                        if test.startswith("validate-modules:"):
                            continue
                # per_version_ignore_content += f"{f} {test}\n"

        ignore_file = ignore_dir / f"ignore-{version}.txt"
        # ignore_file.write_text(per_version_ignore_content)

    info = VersionInfo("amazon_cloud_code_generator")
    dev_md = args.target_dir / "dev.md"
    dev_md.write_text(
        (
            "The modules are autogenerated by:\n"
            "https://github.com/ansible-collections/amazon_cloud_code_generator\n"
            ""
            f"version: {info.version_string()}\n"
        )
    )
    dev_md = args.target_dir / "commit_message"
    dev_md.write_text(
        (
            "bump auto-generated modules\n"
            "\n"
            "The modules are autogenerated by:\n"
            "https://github.com/ansible-collections/amazon_cloud_code_generator\n"
            ""
            f"version: {info.version_string()}\n"
        )
    )

    module_utils_dir = args.target_dir / "plugins" / "module_utils"
    module_utils_dir.mkdir(exist_ok=True)
    vmware_rest_dest = module_utils_dir / "core.py"
    vmware_rest_dest.write_bytes(
        pkg_resources.resource_string(
            "amazon_cloud_code_generator", "module_utils/core.py"
        )
    )


if __name__ == "__main__":
    main()