#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Scaleway

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: scaleway_vpcgw_pat_rule
short_description: Manage Scaleway vpcgw's pat_rule
description:
    - This module can be used to manage Scaleway vpcgw's pat_rule.
version_added: "2.1.0"
author:
    - Nathanael Demacon (@quantumsheep)
extends_documentation_fragment:
    - quantumsheep.scaleway.scaleway
    - quantumsheep.scaleway.scaleway_waitable_resource
requirements:
    - scaleway >= 0.6.0
options:
    state:
        description:
            - Indicate desired state of the target.
            - C(present) will create the resource.
            - C(absent) will delete the resource, if it exists.
        default: present
        choices: ["present", "absent", "]
        type: str
    id:
        type: str
        required: false
    gateway_id:
        type: str
        required: true
    public_port:
        type: int
        required: true
    private_ip:
        type: str
        required: true
    private_port:
        type: int
        required: true
    protocol:
        type: str
        required: true
        choices:
            - unknown
            - both
            - tcp
            - udp
    zone:
        type: str
        required: false
"""

RETURN = r"""
---
pat_rule:
    description: The pat_rule information
    returned: when I(state=present)
    type: dict
    sample:
        id: 00000000-0000-0000-0000-000000000000
        gateway_id: 00000000-0000-0000-0000-000000000000
        created_at: "aaaaaa"
        updated_at: "aaaaaa"
        public_port: 3
        private_ip: "aaaaaa"
        private_port: 3
        protocol: both
        zone: "aaaaaa"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.quantumsheep.scaleway.plugins.module_utils.scaleway import (
    scaleway_argument_spec,
    scaleway_waitable_resource_argument_spec,
    scaleway_get_client_from_module,
    scaleway_pop_client_params,
    scaleway_pop_waitable_resource_params,
)

from scaleway import Client, ScalewayException
from scaleway.vpcgw.v1 import VpcgwV1API


def create(module: AnsibleModule, client: Client) -> None:
    api = VpcgwV1API(client)

    id = module.params.pop("id", None)
    if id is not None:
        resource = api.get_pat_rule(pat_rule_id=id)

        if module.check_mode:
            module.exit_json(changed=False)

        module.exit_json(changed=False, data=resource)

    if module.check_mode:
        module.exit_json(changed=True)

    resource = api.create_pat_rule(**module.params)

    module.exit_json(changed=True, data=resource)


def delete(module: AnsibleModule, client: Client) -> None:
    api = VpcgwV1API(client)

    id = module.params["id"]

    if id is not None:
        resource = api.get_pat_rule(pat_rule_id=id)
    else:
        module.fail_json(msg="id is required")

    if module.check_mode:
        module.exit_json(changed=True)

    api.delete_pat_rule(pat_rule_id=resource.id)

    module.exit_json(
        changed=True,
        msg=f"vpcgw's pat_rule {resource.id} deleted",
    )


def core(module: AnsibleModule) -> None:
    client = scaleway_get_client_from_module(module)

    state = module.params.pop("state")
    scaleway_pop_client_params(module)
    scaleway_pop_waitable_resource_params(module)

    if state == "present":
        create(module, client)
    elif state == "absent":
        delete(module, client)


def main() -> None:
    argument_spec = scaleway_argument_spec()
    argument_spec.update(scaleway_waitable_resource_argument_spec())
    argument_spec.update(
        state=dict(type="str", default="present", choices=["absent", "present"]),
        id=dict(type="str"),
        gateway_id=dict(type="str", required=True),
        public_port=dict(type="int", required=True),
        private_ip=dict(type="str", required=True),
        private_port=dict(type="int", required=True),
        protocol=dict(
            type="str", required=True, choices=["unknown", "both", "tcp", "udp"]
        ),
        zone=dict(type="str", required=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    core(module)


if __name__ == "__main__":
    main()
