GLOBAL_HOOKS = {
    "beaker_log": {
        "name": "beaker_log",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "boot_log.yml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "os_server_boot_log": {
        "name": "os_server_boot_log",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "boot_log.yml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "check_ssh": {
        "name": "check_ssh",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "check_ssh.yaml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "ping": {
        "name": "ping",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "ping.yaml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "port_up": {
        "name": "port_up",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "port_up.yaml",
                "extra_vars": {
                    "port": 22,
                }
            }
        ]
    }
}
