# Support for Oracle Cloud Infrastructure

The starter kit now comes with the [Oracle Cloud Infrastructure](https://cloud.oracle.com) (OCI) [Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io) preinstalled.

1. Follow the instructions on OCI's [Tools Configuration](https://docs.cloud.oracle.com/iaas/Content/ToolsConfig.htm) page to generate, upload the API key and configure the SDK.
1. Place the API key and `config` file in a subdirectory `.oci`, under the home directory of the user. In Mac and Linux, the home directory is expressed by the environment variable `$HOME`, and in Windows, `%USERPROFILE%`.
1. Uncomment the following line in [devcontainer.json](../.devcontainer/devcontainer.json):
    ```json
    "-v", "${env:HOME}${env:USERPROFILE}/.oci:/home/vscode/.oci",
    ```

Running the following Python code should return the user object if the SDK is configured correctly:

```python
import oci

config=oci.config.from_file("~/.oci/config", "DEFAULT")
identity = oci.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data
print(user)
```