#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated by amazon_cloud_code_generator.
# See: https://github.com/ansible-collections/amazon_cloud_code_generator

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
module: logs_log_group
short_description: Create and manage log groups
description:
- Create and manage log groups.
options:
    data_protection_policy:
        description:
        - The body of the policy document you want to use for this topic.
        - You can only add one policy per topic.
        - The policy must be in JSON string format.
        - 'Length Constraints: Maximum length of 30720.'
        type: dict
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    kms_key_id:
        description:
        - The Amazon Resource Name (ARN) of the CMK to use when encrypting log data.
        type: str
    log_group_name:
        description:
        - The name of the log group.
        - If you dont specify a name, AWS CloudFormation generates a unique ID for
            the log group.
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    retention_in_days:
        choices:
        - 1
        - 3
        - 5
        - 7
        - 14
        - 30
        - 60
        - 90
        - 120
        - 150
        - 180
        - 365
        - 400
        - 545
        - 731
        - 1827
        - 2192
        - 2557
        - 2922
        - 3288
        - 3653
        description:
        - The number of days to retain the log events in the specified log group.
        - 'Possible values are: C(1), C(3), C(5), C(7), C(14), C(30), C(60), C(90),
            C(120), C(150), C(180), C(365), C(400), C(545), C(731), C(1827), and C(3653).'
        type: int
    state:
        choices:
        - present
        - absent
        - list
        - describe
        - get
        default: present
        description:
        - Goal state for resource.
        - I(state=present) creates the resource if it doesn't exist, or updates to
            the provided state if the resource already exists.
        - I(state=absent) ensures an existing instance is deleted.
        - I(state=list) get all the existing resources.
        - I(state=describe) or I(state=get) retrieves information on an existing resource.
        type: str
    tags:
        aliases:
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        type: dict
    wait:
        default: false
        description:
        - Wait for operation to complete before returning.
        type: bool
    wait_timeout:
        default: 320
        description:
        - How many seconds to wait for an operation to complete before timing out.
        type: int
author: Ansible Cloud Team (@ansible-collections)
version_added: TODO
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
'''

EXAMPLES = r'''
'''

RETURN = r'''
result:
    description:
        - When I(state=list), it is a list containing dictionaries of resource information.
        - Otherwise, it is a dictionary of resource information.
        - When I(state=absent), it is an empty dictionary.
    returned: always
    type: complex
    contains:
        identifier:
            description: The unique identifier of the resource.
            type: str
        properties:
            description: The resource properties.
            type: dict
'''

import json

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.cloud.plugins.module_utils.core import CloudControlResource
from ansible_collections.amazon.cloud.plugins.module_utils.core import snake_dict_to_camel_dict
from ansible_collections.amazon.cloud.plugins.module_utils.core import ansible_dict_to_boto3_tag_list


def main():

    argument_spec = dict(
       state=dict(type='str', choices=['present', 'absent', 'list', 'describe', 'get'], default='present'),
    )
        
    argument_spec['log_group_name'] = {'type': 'str'}
    argument_spec['kms_key_id'] = {'type': 'str'}
    argument_spec['data_protection_policy'] = {'type': 'dict'}
    argument_spec['retention_in_days'] = {'type': 'int', 'choices': [1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 2192, 2557, 2922, 3288, 3653]}
    argument_spec['tags'] = {'type': 'dict', 'aliases': ['resource_tags']}
    argument_spec['state'] = {'type': 'str', 'choices': ['present', 'absent', 'list', 'describe', 'get'], 'default': 'present'}
    argument_spec['wait'] = {'type': 'bool', 'default': False}
    argument_spec['wait_timeout'] = {'type': 'int', 'default': 320}
    argument_spec['force'] = {'type': 'bool', 'default': False}
    argument_spec['purge_tags'] = {'type': 'bool', 'default': True}


    required_if = [
        ['state', 'present', ['log_group_name'], True],['state', 'absent', ['log_group_name'], True],['state', 'get', ['log_group_name'], True]
    ]
    mutually_exclusive = [
        
    ]

    module = AnsibleAWSModule(argument_spec=argument_spec, required_if=required_if, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    cloud = CloudControlResource(module)

    type_name = 'AWS::Logs::LogGroup'

    params = {}
        
    params['data_protection_policy'] = module.params.get('data_protection_policy')
    params['kms_key_id'] = module.params.get('kms_key_id')
    params['log_group_name'] = module.params.get('log_group_name')
    params['retention_in_days'] = module.params.get('retention_in_days')
    params['tags'] = module.params.get('tags')

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = {k: v for k, v in params.items() if v is not None}

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(
            module.params["tags"]
        )

    params_to_set = snake_dict_to_camel_dict(_params_to_set, capitalize_first=True)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = ['log_group_name']

    # Necessary to handle when module does not support all the states
    handlers = ['create', 'read', 'update', 'delete', 'list']

    state = module.params.get('state')
    identifier = ['log_group_name']
    
    results = {"changed": False, "result": {}}

    if state == "list":
        if "list" not in handlers:
            module.exit_json(**results, msg=f"Resource type {type_name} cannot be listed.")
        results["result"] = cloud.list_resources(type_name, identifier)

    if state in ("describe", "get"):
        if "read" not in handlers:
            module.exit_json(**results, msg=f"Resource type {type_name} cannot be read.")
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "present":
        results = cloud.present(type_name, identifier, params_to_set, create_only_params)

    if state == "absent":
        results["changed"] |= cloud.absent(type_name, identifier)

    module.exit_json(**results)


if __name__ == '__main__':
    main()