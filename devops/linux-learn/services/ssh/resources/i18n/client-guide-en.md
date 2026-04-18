---
Title: Complete Guide to Using an SSH Client
SourceBlob: a471b57366f81e12652fcb7930461c6bc4b69eca
---

```
BriefIntroduction: SSH configuration on the client side
```

<!-- split -->

# Authentication

When we use SSH to connect to a remote server, we usually need to enter a username and password to log in.

However, this can easily lead to security issues. For example, a server with a public IP may be exposed to password brute-force attacks. For security reasons, we can use SSH keys instead.

# generate ssh key

```bash
ssh-keygen -t rsa -b 4096 -C "note" -f ~/.ssh/<key-filename>
```

`-t`: type, specifies the algorithm, here `rsa`

`-b`: bits, specifies the security level in bits; for RSA, at least 2048 is recommended

`-C`: comments

`-f`: specifies the output filename

This will generate `~/.ssh/<key-filename>` (private key) and `~/.ssh/<key-filename>.pub` (public key).

During generation, you can choose whether to protect the private key with a passphrase. If you do, you will need to enter the passphrase when logging in.

In general, the comment we write (`note`) is usually recorded at the end of the public key file, and you can open the `.pub` file directly to check it.

For the filename, it is best to use something meaningful, such as `Singapore-Linux-VM-SSH-Key`.

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
> If you run this command in Windows PowerShell, it may fail after prompting you for the passphrase twice and show an error:
>
> ```powershell
> Generating public/private rsa key pair.
> Enter passphrase (empty for no passphrase):
> Enter same passphrase again:
> Saving key "~/.ssh/github-ssh-key" failed: No such file or directory
> ```
>
> This happens because in some versions of PowerShell, the `~` symbol is not expanded by PowerShell before being passed to the command.
>
> For example: [Powershell does not expand '~' for external programs · Issue #20031 · PowerShell/PowerShell](https://github.com/PowerShell/PowerShell/issues/20031)

## add ssh key to remote server

Now that the SSH key has been generated, we need to add the public key to the remote server.

### command

```shell
ssh-copy-id -p <ssh-port> -i ~/.ssh/Singapore_Linux_VM_SSH_Key.pub <username>@<remote-server-ip>
```

If you are using the default port `22`, you can omit the `-p <ssh-port>` parameter.

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
> - In Windows PowerShell, you cannot use the `ssh-copy-id` command. In that case, you can open Git Bash and run it there.
>
> - If password login has been disabled on the server, this command will likely fail. You might be able to try this command instead:
>
>   ```shell
>   ssh-copy-id -i new-key.pub -o "IdentityFile=old-key" -p <port> user@IP
>   ```
>
>   You can try it next time; I have not tested it myself yet.

### manual

If the command-based method does not work, you can manually add the public key to the server.

First log in to the server, open the `~/.ssh/authorized_keys` file, and paste in the contents of the `.pub` file.

## azure vm

If you are using an Azure Linux VM, you can add the SSH public key in the Azure Portal.

![azure ssh key add](./resources/images/azure-ssh-key-add.png)

## gcp vm

In GCP, you need to go to the VM instance edit page:

![ssh-1](./resources/images/gcp-vm-ssh-1.png)

After entering edit mode, scroll down and you will see the SSH key section.

![ssh-1](./resources/images/gcp-vm-ssh-2.png)

## ssh-key login

If we directly use `ssh username@remote-server-ip`, SSH will only try default-named keys such as `id_rsa` by default.

So we need to specify the key temporarily on the command line:

```javascript
ssh -i ~/.ssh/id_rsa_remote_server username@remote-server-ip
```

Of course, for convenience, we usually add a configuration to `~/.ssh/config` so that SSH automatically knows which key to use for that connection. For example:

```javascript
Host remote-server
    HostName remote-server-ip
    User username
    IdentityFile ~/.ssh/id_rsa_remote_server
```

Then you can simply use `ssh remote-server`, and it will automatically use that key.

# Key Management

SSH Agent is used to store decrypted private keys in memory, so you only need to enter the passphrase once and can reuse the key throughout the session.

In other words, if the private key has no passphrase, you do not need SSH Agent, because SSH can read the private key file directly.

If the private key has a passphrase, then without SSH Agent you need to enter it every time you connect with SSH. With SSH Agent, you only need to enter it once when adding the key to the agent.

## Windows Setup

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

Check which SSH keys have already been added:

```powershell
ssh-add -l
```

## Linux Setup

First, check whether `ssh-agent` is already running:

```shell
echo $SSH_AGENT_PID
```

If `ssh-agent` is running, it will display its process ID (PID); if it is not running, the output will be empty.

If the output is empty, use the following command to start `ssh-agent`:

```bash
eval "$(ssh-agent -s)"
```

Add the SSH private key:

```bash
ssh-add ~/.ssh/<ssh-key-filename> 
```

## Persistence

To make this persistent, you can add these commands to your shell configuration file. Depending on which shell you use, that may be:

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

With this setup, every time you open a new terminal session, `ssh-agent` will start automatically, and your SSH key can then be added.

# Configuration

The default path of the SSH configuration file is usually `~/.ssh/config`. This file is essentially the global configuration file for the SSH client and supports many features.

But first, let’s look at its most basic function: simplifying connection commands by turning a complex set of SSH parameters into a single host alias, so you can log in quickly with `ssh <Host>` instead of entering a long command every time.

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

   After successful authentication, the SSH client automatically stores the decrypted key in `ssh-agent` (if `ssh-agent` is not running at that time, this will not take effect).

   Without this line, `ssh-agent` will not automatically receive your key when you connect to the server with SSH, which means you need to run `ssh-add` manually for that key.

2. ServerAliveInterval 20

   The SSH client sends an application-layer heartbeat packet to the server every 20 seconds to prevent the connection from being reclaimed as an idle connection.

3. ServerAliveCountMax 6

   The SSH client disconnects only after 6 consecutive heartbeats receive no reply, which helps avoid immediate disconnection during brief network instability.

4. TCPKeepAlive yes

   Enables keepalive at the operating system TCP layer.

5. IPQoS none

   Does not set DSCP/QoS markings for SSH traffic. This avoids disconnections or throttling caused by some network devices mishandling certain QoS markings.

> [!tip]
>
> In the VS Code Remote-SSH extension, using `Remote-SSH: Open SSH Configuration File...` edits this same file.

By editing this file, we can specify different private keys for different hosts, such as using separate keys for personal servers and company servers, or different keys for GitHub and GitLab.

```
Host github.com
  User git
  IdentityFile ~/.ssh/github_key  # dedicated GitHub key

Host company-server
  HostName example.com
  User dev
  IdentityFile ~/.ssh/work_key    # company server key
```

> [!important]
>
> Note that SSH config does not support configuring passwords directly.
