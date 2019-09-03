# Oracle Database Connection with Oracle Wallet

This guide assumes the following:

1. The Oracle Database runs on a Docker container named *axer* and is attached to the Docker network *axer_network*.
1. The devcontainer is attached to the Docker network *axer_network*

| Name | Value | Remarks |
|-|-|-|
| PROJECT_ROOT | /home/oracledev/vscode-remote-oradev-python | Direcotry where this repository was cloned to. |
| DB_CONTAINER_NAME | axer | Name of the Oracle Database Docker container. |
| DOCKER_NETWORK | axer_network | Name of the Docker network. Both the database and devcontainer are attached to this network. |
| DB_PORT | 1521 | Database port |
| DB_USERNAME | pydev | Example database username. |
| DB_PASSWORD | pydev123 | Example database password. | 
| WALLET_NAME | pydev_wallet | Name for the wallet. |
| WALLET_PASSWORD | Oracle1# | Password for the wallet. |

*On the host system*:

1. Set the environment variables and working directory:
    ```bash
    $ PROJECT_ROOT=/home/oracledev/vscode-remote-oradev-python
    $ DB_CONTAINER_NAME=axer
    $ DB_PORT=1521
    $ DB_USERNAME=pydev
    $ DB_PASSWORD=pydev123
    $ WALLET_NAME=pydev_wallet
    $ WALLET_PASSWORD=Oracle1#
    $ cd $PROJECT_ROOT
    ```
1. Create a Bash session on the database container.
    ```bash
    $ docker exec -it -u oracle -w /home/oracle \
    >   -e DB_CONTAINER_NAME=$DB_CONTAINER_NAME \
    >   -e DB_PORT=$DB_PORT \
    >   -e DB_USERNAME=$DB_USERNAME \
    >   -e DB_PASSWORD=$DB_PASSWORD \
    >   -e WALLET_NAME=$WALLET_NAME \
    >   -e WALLET_PASSWORD=$WALLET_PASSWORD \
    >   $DB_CONTAINER_NAME bash
    ```
1. (In the database container) Set the Oracle environment variables:
    ```bash
    [oracle@044eeee405b9 /]$ ORAENV_ASK=NO && ORACLE_SID=XE && . oraenv
    The Oracle base remains unchanged with value /opt/oracle
    ```
1. Create a new wallet:
    ```bash
    [oracle@044eeee405b9 /]$ (echo "$WALLET_PASSWORD"; echo "$WALLET_PASSWORD") | mkstore -wrl "$HOME/$WALLET_NAME" -create
    ```
1. Create a database credential entry using either methods of specifying the Easy Connect string:
    ```bash
    [oracle@044eeee405b9 /]$ echo "$WALLET_PASSWORD" | mkstore -wrl "$HOME/$WALLET_NAME" -createCredential $DB_CONTAINER_NAME:$DB_PORT/XEPDB1 $DB_USERNAME $DB_PASSWORD
    ```
1. Check that the credentials were successfully added:
    ```bash
    [oracle@044eeee405b9 /]$ echo $WALLET_PASSWORD | mkstore -wrl "$HOME/$WALLET_NAME" -listCredential
    ```
1. Logout of the database container.
    ```bash
    [oracle@044eeee405b9 /]$ exit
    ```
1. Create a `.wallets` directory and copy the wallet directory and contents:
    ```bash
    $ mkdir .wallets && docker cp $DB_CONTAINER_NAME:/home/oracle/$WALLET_NAME .wallets
    ```
1. Create a `sqlnet.ora` file in the `PROJECT_ROOT`:
    ```bash
    $ cat << EOF > sqlnet.ora
    WALLET_LOCATION =
        (SOURCE =
            (METHOD = FILE)
            (METHOD_DATA =
                (DIRECTORY = .wallets/$WALLET_NAME)
            )
        )
    SQLNET.WALLET_OVERRIDE = TRUE
    EOF
    ```

When executing the Python code, set the `TNS_ADMIN` environment variable to the directory where the `sqlnet.ora` file is located. It is important to note that when running the code within the devcontainer, the `PROJECT_ROOT` is mounted and the current working directory is set to typically a path like `/workspace/vscode-remote-oradev-python`. The leaf of the workspace path follows the name of the running devcontainer name.

When debugging code, add the following attributes to the [`launch.json`](../.vscode/launch.json) file, and update `DB_HOST` (set to the `DB_CONTAINER_NAME` when working with a database container), `DB_PORT` and `DB_SERVICE_NAME` accordingly:

```json
"env": { 
    "TNS_ADMIN": "${cwd}",
    "DB_HOST": "axer",
    "DB_PORT": "1521",
    "DB_SERVICE_NAME": "XEPDB1"
}
```
