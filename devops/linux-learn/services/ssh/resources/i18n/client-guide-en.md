---
Title: Complete SSH Client Guide
SourceBlob: 22fcb7f0469ea838c15c43a16a1571e628bad136
---

```
BriefIntroduction: SSH client configuration guide
```

<!-- split -->

# Authentication

When we use SSH to connect to a remote server, we usually need to enter a username and password to log in.

However, this can create security risks. For example, a server with a public IP may be exposed to password brute-force attacks. For better security, we can use an SSH key.

# Generate SSH Key

```bash
ssh-keygen -t rsa -b 4096 -C "note" -f ~/.ssh/<key-filename>
```

`-t`: type, specifies the algorithm, here `rsa`

`-b`: bits, specifies the security bit length. For RSA, at least 2048 is recommended.

`-C`: comments

`-f`: file, specifies the output file name

This will generate `~/.ssh/<key-filename>` (private key) and `~/.ssh/<key-filename>.pub` (public key).

During generation, we can choose whether to add a passphrase to the private key. If a passphrase is added, you need to enter it during login to decrypt the private key.

The comment we write (`note`) is recorded at the end of the public key file. You can open the `.pub` file directly to check it.

For the file name, it is best to use a meaningful name, such as `Singapore-Linux-VM-SSH-Key`.

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
> In a Windows PowerShell environment, this command may fail after asking you to enter the passphrase twice and then report an error:
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

If you are using the default port 22, you can omit the `-p <ssh-port>` parameter.

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
> - In a Windows PowerShell environment, the `ssh-copy-id` command is not available. In this case, you can open Git Bash and run the command there.

### Manual

If the command method does not work, we can manually add the public key to the server.

First log in to the server, open the `~/.ssh/authorized_keys` file, and copy the contents of the `.pub` file into it.

## Azure VM

If you are using an Azure Linux VM, you can add the SSH public key in the Azure portal.

![azure ssh key add](./resources/images/azure-ssh-key-add.png)

## GCP VM

In GCP, you need to go to the VM instance edit page:

![ssh-1](./resources/images/gcp-vm-ssh-1.png)

After entering edit mode, scroll down and you will see the SSH key section.

![ssh-1](./resources/images/gcp-vm-ssh-2.png)

## SSH Key Login

If we directly use `ssh username@remote-server-ip`, SSH will, by default, only try keys with default names such as `id_rsa`.

So we need to specify the key in the command line:

```javascript
ssh -i ~/.ssh/id_rsa_remote_server username@remote-server-ip
```

For convenience, we usually add configuration to `~/.ssh/config` so SSH automatically knows which key to use for the request. For example:

```javascript
Host remote-server
    HostName remote-server-ip
    User username
    IdentityFile ~/.ssh/id_rsa_remote_server
```

Then you only need to run `ssh remote-server`, and SSH will automatically use that key.

# Key Management

SSH Agent is used to store decrypted private keys. It caches decrypted private keys in memory, so you only need to enter the passphrase once and can reuse the key during the session.

In other words, if the private key has no password, SSH Agent is not needed because SSH can read the private key file directly.

If the private key has a password, without SSH Agent you need to enter the password every time you use SSH to connect. With SSH Agent, you only need to enter the password once when adding the key to the Agent.

## Windows Setting

Check the ssh agent service:

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

Add the ssh key to ssh agent:

```powershell
ssh-add C:\Users\<username>\.ssh\github-ssh-key
```

View the ssh keys that have already been added:

```powershell
ssh-add -l
```

## Linux Setting

First, check whether ssh-agent has already started:

```shell
echo $SSH_AGENT_PID
```

If `ssh-agent` is running, its process ID (PID) will be displayed. If it is not running, the output will be empty.

If the output is empty, start ssh-agent with the following command:

```bash
eval "$(ssh-agent -s)"
```

Add the SSH private key:

```bash
ssh-add ~/.ssh/<ssh-key-filename> 
```

## Persistence

To make this persistent, you can add these commands to your shell configuration file. Depending on the shell you use, this can be:

For Bash (`~/.bashrc` or `~/.bash_profile`):

```bash
if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval "$(ssh-agent -s)"
fi
```

After saving the file, reload the configuration:

```bash
source ~/.bashrc  # 如果使用 bash
```

After this setup, every time you open a new terminal session, ssh-agent will start automatically and add your SSH key.

# Configuration

The default path of the ssh configuration file is usually `~/.ssh/config`. This file is essentially the global configuration file for the SSH client and supports many features.

But first, let’s look at its most basic function: simplifying connection commands. It converts complex SSH command parameters into a host entry, allowing you to log in quickly with `ssh <Host>` without entering a series of complex parameters every time.

By editing this file, we can specify private keys for different hosts. For example, we can use different keys for personal servers and company servers, or configure different keys for GitHub and GitLab.

A classic configuration looks like this:

```json
Host <name>
    HostName <public-ip/private-ip>
    User <username>
    Port <ssh-port>
    IdentityFile ~/.ssh/id_rsa
	AddKeysToAgent yes
	IdentitiesOnly yes
	ServerAliveInterval 20
	ServerAliveCountMax 6
	TCPKeepAlive yes
	IPQoS none
```

1. IdentityFile ~/.ssh/id_rsa

   Try this key first.

2. AddKeysToAgent yes

   After successful authentication, the ssh client automatically stores the decrypted key in ssh-agent. If ssh-agent is not running at the time, this will not take effect.

   Without this line, ssh-agent will not automatically obtain your key when you connect to the server via ssh. In other words, you would need to manually run `ssh-add` for that key.

3. IdentitiesOnly yes

   During connection, only use the `~/.ssh/id_rsa` key for public key authentication. Do not try any additional keys.

4. ServerAliveInterval 20

   The SSH client sends an application-layer heartbeat packet to the server every 20 seconds to prevent the connection from being treated as idle and reclaimed.

5. ServerAliveCountMax 6

   The ssh client disconnects only after 6 consecutive heartbeats receive no response, preventing immediate disconnection during temporary network instability.

6. TCPKeepAlive yes

   Enable keepalive at the operating system TCP layer.

7. IPQoS none

   Do not set DSCP/QoS tags for SSH traffic. This can bypass disconnections or speed limits caused by certain network devices mishandling specific QoS tags.

> [!tip]
>
> In VS Code’s Remote-SSH extension, `Remote-SSH: Open SSH Configuration File...` edits this same file.
>
> After modifying `~/.ssh/config`, new SSH connections take effect immediately. You do not need to restart Windows, and usually do not need to restart ssh-agent.
