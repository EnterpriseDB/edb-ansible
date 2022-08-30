# setup_cloudnativepg_sandbox

This Ansible Galaxy Role Removes CloudNativePG Sandbox.

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

The `setup_cloudnativepg_sandbox` role does not have any dependencies on any other roles.

## Example Playbook

## How to include the `setup_cloudnativepg_sandbox` role in your Playbook

Below is an example of how to include the `setup_cloudnativepg_sandbox` role:

```yaml
---
- hosts: localhost
  name: Deploy CloudNativePG-Sandbox Playbook
  gather_facts: yes

  roles:
    - setup_cloudnativepg_sandbox
```

## Get credentials for Kubernetes Cluster

A previously provisioned Cloud Kubernetes Cluster is required.
The steps below will retrieve the credentials and update the local kubeconfig file.

### AWS EKS - Elastic Kubernetes Service
```bash
# Update local kubeconfig with Cloud Kubernetes Cluster credentials
$ eksctl get nodegroup --cluster <k8s-cluster-name>
```

### Azure Kubernetes Service
```bash
# Update local kubeconfig with Cloud Kubernetes Cluster credentials
$ az aks get-credentials --resource-group <k8s-resource-group> --name <k8s-cluster-name>
```

### Google Kubernetes Engine
```bash
# Update local kubeconfig with Cloud Kubernetes Cluster credentials
$ gcloud container clusters get-credentials <k8s-cluster-name> --region <gcloud-region>
```

## Get the matching `cnp` playbook

Copy the `setup_cloudnativepg_sandbox.yml` playbook located in the `playbook-examples/cnp` directory into the root of the `edb-ansible` directory.

## Playbook execution examples

```bash
# To Deploy CloudNativePG Sandbox into Kubernetes Cluster
$ ansible-playbook setup_cloudnativepg_sandbox.yml 
```

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * DevOps
  * edb-devops@enterprisedb www.enterprisedb.com
