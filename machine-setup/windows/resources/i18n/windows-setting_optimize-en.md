---
Title: Windows System Settings
SourceBlob: 5cb246707db538e7d9a0774464bcebab76a02fb8
---

```
BriefIntroduction: Some settings to configure on a clean Windows installation after reinstalling the system.
```

<!-- split -->

# Windows 10 Settings

First are some system settings. This section refers to a Bilibili video[^Bilibili].

1. Change the computer name

   Press `Win + I` to open Settings, click the first item, `System`, then scroll to the bottom of the left sidebar and open `About`. There you can see the option to rename this PC.

   ![settings](./resources/images/setting.png)

   ![rename](./resources/images/rename.png)

   Restart the computer after renaming it.

2. Rename the user account

   Refer to this article: [windows - Change the user account name (Windows 10)_Change Windows username_CSDN Blog](https://blog.csdn.net/weixin_44198965/article/details/115689689)

## Taskbar Settings

Find the taskbar at the bottom of Windows and right-click it. Disable anything you do not want to display. I usually keep it like this.

<img src=".\images\TaskBar.png" alt="image-20231004011419683" style="zoom:75%;" />

Click `Search (H)`, and I choose to hide the search icon because it is not very useful. I often use `Win + Space` for search instead. Click `News and interests (N)`, and I choose to turn it off. Then click `Taskbar settings (T)` at the bottom.

Under `Notification area --> Turn system icons on or off`, keep only the icons you want.

Turn off the `News and interests` and `People` section.

As for the apps in the lower-left corner, set them however you like.

## System Settings

Open Settings (`Win + I`).

1. Remove apps

   Find `Apps` and uninstall anything you do not want or do not like. Generally, if you used the official Microsoft installation image, there will not be that many extra apps.

2. Privacy settings

   Go to `Privacy settings --> General` and turn off all tracking options.

   Turn off `Contacts` and `Phone calls`.

   Under `Background apps`, turn off software you do not use often.

3. Start menu settings

   Press the `Win` key to open the Start menu, select the Settings icon, right-click it, and choose `Personalize`. You can choose which icons appear on the Start menu.

![start menu settings](./resources/images/start-menu-setting.png)

Personally, I only keep the Settings option.

![start menu](./resources/images/start-menu-setting-1.png)

## File Explorer Settings

`View --> Options --> Open File Explorer to: This PC`

![file explorer](./resources/images/filesystem-setting-0.png)

At the same time, I disable `Show frequently used folders` and `Show recently used files` in Quick Access, and I also remove the four pinned items in Quick Access.

![file explorer](./resources/images/filesystem-setting-1.png)

For the five system folders on the left side, `Videos`, `Documents`, `Downloads`, `Music`, and `Pictures`, change their paths to drive `E:`.

Create five folders with the same names on drive `E:`, then select `Videos` on the left, right-click it, choose `Properties --> Location --> Move`, and select the newly created folder with the same name.

1. About Quick Access

   I usually use it like this: in the `Data` drive, create one frequently used folder, such as `English Vocabulary Notes`, pin it to Quick Access, and then hide it in the `Data` drive. This keeps things clean.

   As mentioned above, I hide the `Downloads`, `Videos`, `Pictures`, and `Music` folders after moving them to the `Data` drive. This way, I can access them directly through `This PC` in the sidebar without opening the `Data` drive.

# Default Applications

Change the default app for opening PDF files to Edge: [How to change the default PDF opener to Edge_win10 PDF always opens with Edge-CSDN Blog](https://blog.csdn.net/nofall_bird/article/details/138244710)

# Activate Windows

[[WeiLingWei]-Windows/Office Full Activation Guide-KMS Online Activation-KMS Activation Server-Windows 11 Permanent Activation with One Command-Windows 10 Permanent Activation with One Command (jihuowin.com)](https://jihuowin.com/index.php)

Refer to this link.

# Startup Programs

In this path:

```text
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
```

You can place startup programs for Windows 10. You can also write your own programs and put shortcuts to them here.

# Reference

[^Bilibili]: [Settings you should change immediately after getting your computer!_bilibili](https://www.bilibili.com/video/BV1am4y1R7pi/?spm_id_from=333.880.my_history.page.click&vd_source=617c4a2b4e326fc6b6269aada0d25986)
