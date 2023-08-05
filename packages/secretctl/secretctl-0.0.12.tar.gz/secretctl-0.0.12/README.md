# secretctl
Command-line tool for working with aws secrets manager.

## Installing

`secretctl` is a python package.

```bash
$ pip install secretctl
```

## Authenticating

'secretctl' requires an authenticated AWS user with permissions to use the Secrets Manager, as resolved by boto3.
The primary example being identity settings in ~/.aws/credentials. A recommended way to do this is using `aws-vault`,
as in:

```bash
$ aws-vault exec prod -- secretctl ..
```

## Usage

### Creating and Updating Secrets

```bash
$ secretctl create <path/key> <value | ->
```

This command will write a secret into the Secret Managers. If `-` is provided as the value argument, the value will be read from standard input. A description can be added using the --description flag. Tags are added using the --tags flag
and flag values in the tag=value format.

```bash
$ secretctl create <path/key> <value> --description <STRING> --tags <tag>=<value>, ..
```

If the path/key already exists, the process will fail. Use `update` to change the value of a
secret.

```bash
$ cat <filename> | secretctl update myapp/dev/public-key -
```
Use `secretctl tag` and `secretctl untag` to add/remove/modify tags.

### Reading Secrets

```bash
$ secretctl read myapp/dev/docker_login

   Path/Key                   Version   Value
   myapp/dev/docker_login     1         mydockerlogin
```
Use `--quiet` to return only the secret value.

### Listing Secrets

```bash
$ secretctl list --path di/dev/

Path/Key                Description                             Tags
di/dev/docker_username  access credentials for private regis..  team=di, circleci-context=team-di
di/dev/docker_password  access credentials for private regis..  team=di, circleci-context=team-di
di/dev/vault_token      team vault token                        team=di, circleci-context=team-di
Found 3 secrets.
```

If no --path is provided, all secrets will be listed. Use the --tags <STRING> to filter for secrets where tags or values
match STRING.

### Exporting
```bash
$ secretctl export di/dev/

docker_username=mydockerlogin
docker_password=mydockerpassword
vault_token=myvaulttoken
```

Example use in a deploy pipeline:
```bash
$ secretctl export di/dev/ > local.env
$ source local.env
```

`export` can export secrets in various file formats. The following
file formats are supported:

* tfvars (default)
* json
* csv



### under development

sercretctl does not yet support:
custom KMS key
binary secret value type
(unit testing) no moto support for testing descriptions or resource tags
