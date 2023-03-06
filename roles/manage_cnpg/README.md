# manage_cnpg

This Ansible Galaxy Role contains task files that assist in the management of CloudNativePG and EDB Postgres for Kubernetes.

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
  5. `kubernetes.core.k8s` - Ansible Module - Required for Kubernetes.
  6. CloudNativePG PlugIn is required for: Promoting Pods, Reloading cluster and pods, Restarting Cluster and Pods, Managing Maintenance Modes and Cluster Status.

## Role variables

'cnpg_task' must be defined with a value in order to indicate which task in the role will be executed.
The options are:
- add-db, add-schema, add-role
- drop-db, drop-schema, drop-role
- execute-sql-script
- apply-manifest, remove-manifest
- configure-memory, configure-pg-hba
- scale-replicas
- get-superuser-secret, add-postgres-expose-service, drop-postgres-expose-service
- add-grafana-expose-service, drop-grafana-expose-service
- promote-pod
- reload-cluster, restart-cluster, restart-pod
- maintenance-set, maintenance-unset
- status-cluster


## Dependencies

The `manage_cnpg` role does not have any dependencies on any other roles.

## Example Playbook

## How to include the `manage_cnpg` role in your Playbook

Below is an example of how to include the `manage_cnpg` role:

```yaml
---
- name: Manage a CloudNativePG or CloudNative Postgres Cluster Playbook
  hosts: localhost
  gather_facts: false

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      ansible.builtin.set_fact:
        # Options"
        # add-db, add-schema, add-role
        # drop-db, drop-schema, drop-role
        # execute-sql-script
        # apply-manifest, remove-manifest
        # configure-memory, configure-pg-hba
        cnp_task: 
        - drop-role
        # CloudNativePG Namespace
        cnpg_namespace: default
        # CloudNativePG Cluster Name
        cluster_name: cluster-example
        # CloudNativePG Pod Name
        pod_name: cluster-example-2
        # Databases
        db_name: edb
        # Schemas
        schema_name: edb_schema
        # Roles
        db_role: edb_role
        db_role_password: admin
        # SQL Script
        sql_script: DROP DATABASE {{ db_name }};
        # Manifest Filename
        manifest_filename: configure_memory.yml
        # Scale Replicas Number
        scale_replicas_to: 3
        # Scale Manifest Filename
        scale_manifest_filename: roles/manage_cnpg/files/cluster-example.yml

  roles:
    - role: manage_cnpg
      when: cnp_task is defined
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

## Get the matching `CloudNativePG` playbook

Copy the `manage_cnpg.yml` playbook located in the `playbook-examples/manage_cvnpg` directory into the root of the `edb-ansible` directory.

## Install the `CloudNativePG` PlugIn

Navigate towards: 'https://cloudnative-pg.io/documentation/1.19/cnpg-plugin/' url to find the installation process for your distribution.
The CloudNativePG PlugIn is required for the following tasks: Promoting, Restarting, Reloading, Setting Maintenance Modes, and Status

## Playbook execution examples

```bash
# To Deploy CloudNativePG Sandbox into Kubernetes Cluster
$ ansible-playbook manage_cnpg.yml 
```

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * DevOps
  * edb-devops@enterprisedb www.enterprisedb.com
