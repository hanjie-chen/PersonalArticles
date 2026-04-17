<!-- source_blob: 72f7e15e992130db390c11fd9f001dc7b9531a8c -->

# Before We Begin

The author recently built a new PC and downloaded some additional software to make it more pleasant to use. This article is meant to help restore the system to the same familiar setup and style after a future OS reinstall. It may also serve as a reference for others with similar needs.

# Windows Extra Software

Some of the software I am currently using to make Windows more comfortable and efficient.

| Software name                | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| Clash-for-window             | Without this, I couldn't even download Chrome                |
| Chrome Brower                | The best browser on the planet, used to download other software |
| 7-zip                        | Open-source compression and extraction software for Windows  |
| everything                   | Essential for finding files                                  |
| Vmware-workstation           | Virtual machine software; I need one Windows 10 VM for galgames and one Linux VM for development |
| PotPlayer                    | Video player                                                 |
| Typora                       | A fantastic Markdown writing tool; I started with the free 0.7 version and eventually became a paying user |
| YACReader                    | A great local comic reader that can also build a local comic library |
| Visual Studio code (VS code) | A lightweight code editor that works very well on both Windows and macOS |
| Steam                        | A must-have for entertainment                                |
| Windows terminal             | An excellent terminal tool on Windows, especially when combined with `oh-my-posh` |
| Fliqlo                       | Desktop screensaver                                          |
| Mircosoft Todo List          | For setting daily tasks                                      |
| Koodo Reader                 | Open-source reading software for Windows                     |
| codex                        | A powerful tool that tries to help you solve any problem     |
| rime                         | Weasel, an excellent input method                            |

# Software Settings

## Rime

When we use `fu pan` to try typing `复盘`, we find that it fails because of a bug (Traditional Chinese to Simplified Chinese conversion).

We can create a `custom_phrase.txt` file in the user folder with the following content:

```txt
复盘	fupan	100
复盘	fp	100
```

Note: the separators in the middle must be Tab characters, not spaces.

Then right-click Weasel and redeploy it.

### Sync Backup

The sync method officially recommended by Rime for multiple devices is to set `sync_dir` in `installation.yaml`, then use "Synchronize User Data".

The official documentation is very clear: during synchronization, the user dictionary is generated/merged into `*.userdb.txt` snapshots, and non-auto-generated YAML and `.txt` files in the user folder are backed up one-way to the sync directory. Typical files in the sync directory include `installation.yaml`, `default.custom.yaml`, `weasel.custom.yaml`, and `*.userdb.txt`.

1. Open `installation.yaml` in the user folder.
2. Add a line like this:

```yaml
sync_dir: 'D:\OneDrive\backup\Rime\backup'
```

1. Save the file and redeploy.
2. Run "Synchronize User Data" in Weasel.

Note: synchronizing user data includes two actions: pull + push.

It first pulls any existing user dictionary snapshots from the sync directory and merges them into the current dictionary, then pushes the current user configuration and new dictionary snapshots back to the sync directory. If the sync directory is empty, it simply backs up the current configuration there; if it is not empty, it merges first and then backs up.

## Edge Settings

Purpose: prevent searches from being redirected to `cn.bing.com`, and use the new Bing instead.

As the browser built into Windows, Edge may not always be as good as Chrome, but it is still more than enough for everyday use.

The first issue is that Bing forces the search region to China, which prevents access to useful AI tools such as the new Bing.

The reason is the search engine configuration in the address bar. Go to Edge Settings --> Privacy, search, and services --> Address bar and search --> Manage search engines, as shown below.

![search-engine-preview](./resources/images/search-engine-preview.png)

Just modify the query URL (add a new one again and set it as the default).

![search-engine-current](./resources/images/search-engine-current.png)

That should do it. This article was referenced here[^1].

1. Vertical tabs

   <img src="./resources/images/vertical-tab.png" alt="picture" style="zoom:60%;" />

2. Hide the title bar

   <img src="./resources/images/hidden-tablename.png" alt="picture" style="zoom:60%;" />

3. Other settings

   You can explore the other homepage settings on your own.

## Fliqlo Settings

Purpose: launch the desktop screensaver with a global shortcut key (note: this does not work when another application is in full-screen mode).

### Method 1: Pin the Fliqlo shortcut to the Start menu

1. Create a Fliqlo shortcut and place it on the desktop.
2. Open the Start menu folder. This folder is usually located at `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`. Drag the shortcut into it (administrator permission is required).
3. Open the Start menu, find the Fliqlo shortcut, right-click it, and pin it to Start.

### Method 2: Create a desktop shortcut directly, then assign a hotkey

1. Note that with this method, you cannot hide the desktop shortcut. Otherwise, the hotkey will no longer work the next time you try to launch it. This approach leaves a shortcut on the desktop, and since I prefer a cleaner desktop, I abandoned this option.

## Windows Terminal Optimization

Purpose: make the terminal look better and enable built-in administrator privileges on startup.

I mainly use the [oh-my-posh](https://ohmyposh.dev/) theme to improve Windows Terminal.

Then there are some additional Windows Terminal appearance tweaks and command-line completion settings[^2].

```josn
        "defaults": {
          // start transparent effect, set the transparency to 0.9
          "useAcrylic": true, 
          "acrylicOpacity": 0.9,
          "fontFace": "MesloLGM Nerd Font Mono",
          "fontSize": 14
        },
```

For details, see the reference video.

Then, to start with administrator privileges by default, use the `elevate` property so it opens as admin automatically[^3]. I also set the default startup directory to the project folder `E:\\Personal_Project`.

The JSON code is as follows:

```json
            {
                "commandline": "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
                "hidden": false,
                "name": "Windows PowerShell",
                // open the wt default as the administer
                "elevate": true,
                // set the default start directory
                "startingDirectory": "E://Personal_Project"
            }
```

## PotPlayer Settings

Purpose: make the player easier to use.

This software has far too many settings to cover, but the most important ones are hardware decoding (`H/W`, GPU decoding) and software decoding (CPU decoding).

See the reference video[^4] for details.

# Visio

Download and activation: [Microsoft Visio Professional 2019_Visio 2019 - CSDN Blog](https://blog.csdn.net/milkhq/article/details/105714076)

# References

[^1]: [How to configure the Edge search bar](https://answers.microsoft.com/zh-hans/microsoftedge/forum/all/edge使用必应搜/6637cc55-5366-4a01-adc3-fd5db4b666fd)
[^2]: [Tutorial: Beautifying the terminal with Windows Terminal + oh-my-posh - Bilibili](https://www.bilibili.com/video/BV1Qa411T7Au/?spm_id_from=333.337.search-card.all.click&vd_source=617c4a2b4e326fc6b6269aada0d25986)
[^3]: [Open PowerShell as administrator in Windows Terminal - Cyber-Cynic - CNBlogs](https://www.cnblogs.com/talentzemin/p/15930400.html)
[^4]: [Watch TV and slack off too! PotPlayer usage guide & tips - Bilibili](https://www.bilibili.com/video/BV1Tx4y1X7Fh/?spm_id_from=333.337.search-card.all.click&vd_source=617c4a2b4e326fc6b6269aada0d25986)
