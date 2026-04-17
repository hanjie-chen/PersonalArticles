<!-- source_blob: a471b57366f81e12652fcb7930461c6bc4b69eca -->

# Authentication

When we use SSH to connect to a remote server, we usually need to enter a username and password to log in.

However, this can lead to security issues. For example, a server with a public IP may be exposed to password brute-force attacks. For better security, we can use SSH keys.

# Generate SSH Key

```bash
ssh-keygen -t rsa -b 4096 -C "note" -f ~/.ssh/<key-filename>
```

`-t`: type, specifies the RSA algorithm

`-b`: bits, specifies the key size; for RSA, at least 2048 is recommended

`-C`: comments

`-f`: specifies the output file name

This will generate `~/.ssh/<key-filename>` (private key) and `~/.ssh/<key-filename>.pub` (public key).

During generation, you can choose whether to protect the private key with a passphrase. If you do, you will need to enter the passphrase when logging in.

In general, the comment you write (`note`) is usually recorded at the end of the public key file, and you can inspect it by opening the `.pub` file directly.

For the file name, it is best to choose something meaningful, such as `Singapore-Linux-VM-SSH-Key`.

e.g.

```shell
➜ .ssh  ssh-keygen -t rsa -b 4096 -C "Singapore Linux VM" -f ./Singapore_Linux_VM_SSH_Key
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in ./Singapore_Linux_VM_SSH_Key
Your public key has been saved in ./Singapore_Linux_VM_SSH_Key.pub
The key fingerprint is:
SHA256:lcVNmuQlFiyBm6FMZfzL+0uhLVWzftlGcURFXz/t5w8 Singapore Linux VM
The key's randomart image is:
+---[RSA 4096]----+
|       oo..+*+ooB|
|      ..+ .*o=..=|
|     o . =o.+ oo=|
|      o o..  . ++|
|        S. .o . +|
|          o+ o o+|
|          o.o E.=|
|          .o   +.|
|           .o.  .|
+----[SHA256]-----+
```

> [!note]
>
> If you run this command in Windows PowerShell, it may fail and report an error after asking for the passphrase twice:
>
> ```powershell
> Generating public/private rsa key pair.
> Enter passphrase (empty for no passphrase):
> Enter same passphrase again:
> Saving key "~/.ssh/github-ssh-key" failed: No such file or directory
> ```
>
> This is because in some versions of PowerShell, the `~` symbol is not expanded by PowerShell before being passed to the command.
>
> For example: [Powershell does not expand '~' for external programs · Issue #20031 · PowerShell/PowerShell](https://github.com/PowerShell/PowerShell/issues/20031)

## Add SSH Key to Remote Server

Now that the SSH key has been generated, we need to add the public key to the remote server.

### Command

```shell
ssh-copy-id -p <ssh-port> -i ~/.ssh/Singapore_Linux_VM_SSH_Key.pub <username>@<remote-server-ip>
```

If you use the default port `22`, you can omit the `-p <ssh-port>` argument.

e.g.

```shell
$ ssh-copy-id -p <ssh-port> -i ./Singapore_Linux_VM_SSH_Key.pub <username>@<remote-server-ip>
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "./Singapore_Linux_VM_SSH_Key.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
Plain@<remote-server-ip>'s password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh -p <ssh-port> 'Plain@<remote-server-ip>'"
and check to make sure that only the key(s) you wanted were added.
```

> [!note]
>
> - In Windows PowerShell, the `ssh-copy-id` command is not available. In that case, you can open Git Bash and run the command there.
>
> - If password login has been disabled on the server, this command will likely fail. You might be able to try this command instead:
>
>   ```shell
>   ssh-copy-id -i new-key.pub -o "IdentityFile=old-key" -p <port> user@IP
>   ```
>
>   I have not tried it yet, but it may be worth testing next time.

### Manual

If the command approach does not work, you can manually add the public key to the server.

First, log in to the server, open the `~/.ssh/authorized_keys` file, and copy the contents of the `.pub` file into it.

## Azure VM

If you are using an Azure Linux VM, you can add the SSH public key in the Azure portal.

![azure ssh key add](./resources/images/azure-ssh-key-add.png)

## GCP VM

In GCP, you need to go to the VM instance's edit page:

![ssh-1](./resources/images/gcp-vm-ssh-1.png)

After entering the edit page, scroll down and you will see the SSH key section.

![ssh-1](./resources/images/gcp-vm-ssh-2.png)

## SSH Key Login

If we simply use `ssh username@remote-server-ip`, SSH will by default only try keys with default names such as `id_rsa`.

So we need to specify the key temporarily on the command line:

```javascript
ssh -i ~/.ssh/id_rsa_remote_server username@remote-server-ip
```

Of course, for convenience, we usually add configuration in `~/.ssh/config` so that SSH automatically knows which key to use for a given connection. For example:

```javascript
Host remote-server
    HostName remote-server-ip
    User username
    IdentityFile ~/.ssh/id_rsa_remote_server
```

Then you can simply run `ssh remote-server` and the correct key will be used automatically.

# Key Management

SSH Agent is used to store decrypted private keys in memory, so you only need to enter the passphrase once and can reuse the key throughout the session.

In other words, if the private key has no passphrase, you do not need SSH Agent, because SSH can read the private key file directly.

If the private key is encrypted and you do not use SSH Agent, you will need to enter the passphrase every time you connect with SSH. With SSH Agent, you only need to enter it once when adding the key to the agent.

## Windows Setting

Check the SSH Agent service:

```powershell
Get-Service ssh-agent
```

Start the service:

```powershell
Start-Service ssh-agent
```

If needed, set it to start automatically:

```powershell
Set-Service -Name ssh-agent -StartupType Automatic
```

Add an SSH key to the SSH Agent:

```powershell
ssh-add C:\Users\<username>\.ssh\github-ssh-key
```

View the SSH keys that have already been added:

```powershell
ssh-add -l
```

## Linux Setting

First, check whether `ssh-agent` is already running:

```shell
echo $SSH_AGENT_PID
```

If `ssh-agent` is running, it will display its process ID (PID). If it is not running, the output will be empty.

If the output is empty, use the following command to start `ssh-agent`:

```bash
eval "$(ssh-agent -s)"
```

Add the SSH private key:

```bash
ssh-add ~/.ssh/<ssh-key-filename> 
```

## Persistence

To make this persistent, you can add these commands to your shell configuration file. Depending on the shell you use, that might be:

For Bash (`~/.bashrc` or `~/.bash_profile`):

```bash
if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval "$(ssh-agent -s)"
fi
```

After saving the file, reload the configuration:

```bash
source ~/.bashrc  # if using bash
```

With this setup, `ssh-agent` will start automatically every time you open a new terminal session, and your SSH keys can then be added for use.

# Configuration

The SSH configuration file is usually located at `~/.ssh/config`. This file is essentially the global configuration file for the SSH client and supports many features.

But first, let's look at its most basic function: simplifying connection commands. It turns a long and complex SSH command with many parameters into a single host entry, so you can log in quickly with `ssh <Host>` instead of typing the full command every time.

A classic configuration looks like this:

```json
Host <name>
    HostName <public-ip/private-ip>
    User <username>
    Port <ssh-port>
    IdentityFile ~/.ssh/id_rsa
	AddKeysToAgent yes
	ServerAliveInterval 20
	ServerAliveCountMax 6
	TCPKeepAlive yes
	IPQoS none
```

1. AddKeysToAgent yes

   After the SSH client authenticates successfully, it automatically stores the decrypted key in `ssh-agent` (if `ssh-agent` is running; otherwise this will not take effect).

   Without this setting, `ssh-agent` will not automatically receive your key when you connect to a server over SSH, which means you would need to run `ssh-add` manually for that key.

2. ServerAliveInterval 20

   The SSH client sends an application-layer heartbeat to the server every 20 seconds to prevent the connection from being reclaimed as an "idle connection."

3. ServerAliveCountMax 6

   The SSH client disconnects only after 6 consecutive heartbeats receive no response, which helps avoid immediate disconnection during short network interruptions.

4. TCPKeepAlive yes

   Enables keepalive at the operating system's TCP layer.

5. IPQoS none

   Does not set DSCP/QoS markings for SSH traffic. This can avoid disconnects or throttling caused by certain network devices mishandling specific QoS markings.

> [!tip]
>
> In VS Code's Remote-SSH extension, `Remote-SSH: Open SSH Configuration File...` edits this same file.

By editing this file, we can specify different private keys for different hosts, such as using different keys for personal servers and company servers, or different keys for GitHub and GitLab.

```
Host github.com
  User git
  IdentityFile ~/.ssh/github_key  # dedicated key for GitHub

Host company-server
  HostName example.com
  User dev
  IdentityFile ~/.ssh/work_key    # key for the company server
```

> [!important]
>
> Note that `ssh config` does not support configuring passwords directly.
