# remove_cloudnativepostgres_sandbox

This Ansible Galaxy Role Removes CloudNative Postgres Sandbox.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependencies required for this ansible galaxy role are:

  1. AWS EKS CLI, Azure CLI, or Google Cloud CLI - Depends directly on the target cloud
  2. Kubectl
  3. Ansible
  4. Python packages: openshift, pyyaml, kubernetes, pyhelm
     Installed with commands:
     `pip install openshift pyyaml kubernetes`
     `pip install pyhelm`
  5. `kubernetes.core.helm_repository` - Ansible Module - Required for Helm.
  6. `community.kubernetes.helm` - Ansible Module - Required for Helm.
  7. `kubernetes.core.k8s` - Ansible Module - Required for Kubernetes.

## Role variables

There are no required variables:

## Dependencies

The `remove_cloudnativepostgres_sandbox` role does not have any dependencies on any other roles.

## Example Playbook

## How to include the `remove_cloudnativepostgres_sandbox` role in your Playbook

Below is an example of how to include the `remove_cloudnativepostgres_sandbox` role:

```yaml
---
- hosts: localhost
  name: Remove CloudNative Postgres-Sandbox Playbook
  gather_facts: yes

  roles:
    - remove_cloudnativepostgres_sandbox
```

## Get the matching `cnp` playbook

Copy the `remove_cloudnativepostgres_sandbox.yml` playbook located in the `playbook-examples/cnp` directory into the root of the `edb-ansible` directory.

## Playbook execution examples

```bash
# To Remove CloudNative Postres Sandbox from Kubernetes Cluster
$ ansible-playbook remove_cloudnativepostgres_sandbox.yml 
```

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * DevOps
  * edb-devops@enterprisedb www.enterprisedb.com
