---
Title: Additional Windows Software and Settings
SourceBlob: 72f7e15e992130db390c11fd9f001dc7b9531a8c
---

```
BriefIntroduction: After reinstalling Windows and finishing the built-in system setup, there are still some extra apps worth downloading to make the system much smoother to use. I personally prefer open-source software whenever possible.
```

<!-- split -->

# Before We Start

I recently built a new PC, and to make it more pleasant to use, I downloaded some extra software. This article is meant to help me restore my computer to the style and setup I already like and am familiar with after reinstalling the system. It can also serve as a reference for others with similar needs.

# Windows Extra Software

Here is some of the software I am currently using to make Windows more pleasant to use.

| Software name                | Description                                                      |
| ---------------------------- | ---------------------------------------------------------------- |
| Clash-for-window             | Without this, I couldn't even download Chrome                    |
| Chrome Brower                | Arguably the best browser on Earth, used to download other software |
| 7-zip                        | An open-source compression and extraction tool for Windows       |
| everything                   | Essential for finding files                                      |
| Vmware-workstation           | Virtual machine software; I need one Windows 10 VM for galgames and one Linux VM for development |
| PotPlayer                    | Video player                                                     |
| Typora                       | A fantastic Markdown writing tool; I started with the free 0.7 version and eventually became a paying user |
| YACReader                    | A great local comic reader that can also build a local comic library |
| Visual Studio code (VS code) | A lightweight code editor that works very well on both Windows and macOS |
| Steam                        | Great for entertainment                                          |
| Windows terminal             | An excellent terminal tool on Windows; pair it with oh-my-posh for the best experience |
| Fliqlo                       | Desktop screensaver software                                     |
| Mircosoft Todo List          | For setting daily tasks                                          |
| Koodo Reader                 | An open-source reading app for Windows                           |
| codex                        | A powerful tool that tries to help you solve almost any problem  |
| rime                         | Weasel/Rime, an excellent input method                           |

# Software Settings

## Rime

When we use `fu pan` to try to type `复盘`, we find that it fails because of a bug (Traditional Chinese to Simplified Chinese conversion).

We can place a `custom_phrase.txt` file in the user folder with the following content:

```txt
复盘	fupan	100
复盘	fp	100
```

Note: the separators in the middle must be Tabs, not spaces.

Then right-click Weasel and redeploy the service.

### Sync Backup

The synchronization method officially recommended by Rime for multiple devices is to set `sync_dir` in `installation.yaml`, then use "Sync User Data".

The official documentation is very clear: during synchronization, user dictionaries are generated/merged into `*.userdb.txt` snapshots, and non-auto-generated YAML and `.txt` files in the user folder are backed up one-way to the sync directory. Typical files in the sync directory include `installation.yaml`, `default.custom.yaml`, `weasel.custom.yaml`, and `*.userdb.txt`.

1. Open `installation.yaml` in the user folder.
2. Add a line like this:

```yaml
sync_dir: 'D:\OneDrive\backup\Rime\backup'
```

1. Save it and redeploy.
2. Run "Sync User Data" in Weasel.

Note: syncing user data includes two actions: pull + push.

It first pulls the existing user dictionary snapshots from the sync directory and merges them into the current dictionary, then pushes the current user configuration and new dictionary snapshots back to the sync directory. If the sync directory is empty, it simply backs up the current configuration there; if it is not empty, it merges first and then backs up.

## Edge Settings

Purpose: prevent search results from redirecting to `cn.bing.com`, and use the new Bing instead.

As the browser that comes with Windows, Edge may not always be as good as Chrome, but it is still sufficient for everyday use.

The first issue is that Bing forces the search region to China, which makes useful AI tools such as the new Bing unavailable.

The reason lies in the search engine settings for the address bar. Go to Edge Settings --> Privacy, search, and services --> Address bar and search --> Manage search engines, as shown below.

![search-engine-preview](./resources/images/search-engine-preview.png)

You only need to modify the query URL (add a new one again and set it as default).

![search-engine-current](./resources/images/search-engine-current.png)

After that, it should work. I referred to this article[^1].

1. Vertical tabs

   <img src="./resources/images/vertical-tab.png" alt="picture" style="zoom:60%;" />

2. Hide the title bar

   <img src="./resources/images/hidden-tablename.png" alt="picture" style="zoom:60%;" />

3. Other settings

   You can explore the other homepage settings yourself.

## Fliqlo Settings

Purpose: use a global shortcut key to start the desktop screensaver (note that this does not work when software is in full-screen mode).

### Method 1: Pin the Fliqlo shortcut to the Start menu

1. Create a Fliqlo shortcut and place it on the desktop.
2. Open the Start menu folder. This folder is usually located at `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`. Drag the shortcut into it (administrator permission is required).
3. Open the Start menu, find the Fliqlo shortcut, right-click it, and pin it to Start.

### Method 2: Create a desktop shortcut directly, then assign a shortcut key

1. Note that with this method, you cannot hide the desktop shortcut. Otherwise, the shortcut key will not work the next time you try to launch it. This method leaves a shortcut on the desktop, and since I prefer a cleaner desktop, I abandoned this option.



## Windows Terminal Optimization

Purpose: improve the terminal appearance and enable the terminal's built-in administrator privileges.

I mainly use the [oh-my-posh](https://ohmyposh.dev/) theme to improve Windows Terminal.

Then there are some Windows Terminal beautification settings and command-line completion features[^2].

```josn
        "defaults": {
          // start transparent effect, set the transparency to 0.9
          "useAcrylic": true, 
          "acrylicOpacity": 0.9,
          "fontFace": "MesloLGM Nerd Font Mono",
          "fontSize": 14
        },
```

You can check the reference video for details.

Then there is enabling administrator privileges by default, using the `elevate` property so it always opens as administrator[^3], and setting the default startup directory to the project folder `E:\\Personal_Project`.

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

This software has far too many settings, but the most important ones are hardware decoding (H/W, GPU decoding) and software decoding (CPU decoding).

See the reference video for details[^4].

# Visio

Download and activation: [Microsoft Visio 专业版 2019_visio 2019-CSDN博客](https://blog.csdn.net/milkhq/article/details/105714076)

# Reference

[^1]: [how to setting the edge search bar](https://answers.microsoft.com/zh-hans/microsoftedge/forum/all/edge使用必应搜/6637cc55-5366-4a01-adc3-fd5db4b666fd)
[^2]: [【教程】终端美化 Windows Terminal+oh-my-posh美化_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Qa411T7Au/?spm_id_from=333.337.search-card.all.click&vd_source=617c4a2b4e326fc6b6269aada0d25986)
[^3]: [Windows Terminal打开管理员权限的PowerShell - Cyber-Cynic - 博客园 (cnblogs.com)](https://www.cnblogs.com/talentzemin/p/15930400.html)
[^4]:[能看电视，能摸鱼！超强播放器 PotPlayer 使用指南&技巧分享_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Tx4y1X7Fh/?spm_id_from=333.337.search-card.all.click&vd_source=617c4a2b4e326fc6b6269aada0d25986)
