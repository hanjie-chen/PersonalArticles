<!-- source_blob: 5cb246707db538e7d9a0774464bcebab76a02fb8 -->

# Windows 10 Settings

First, here are some system settings. This section references a Bilibili video.[^Bilibili]

1. Change the computer name

   Press `Win + I` to open Settings, click the first item, `System`, then scroll down the left sidebar to `About`. There you can find the option to rename this PC.

   ![setting](./resources/images/setting.png)

   ![rename](./resources/images/rename.png)

   Restart the computer after renaming it.

2. Rename the username

   Refer to this article: [windows - Change User Account Name (Windows 10)_Change Windows Username_CSDN Blog](https://blog.csdn.net/weixin_44198965/article/details/115689689)

## Taskbar Settings

Find the taskbar at the bottom of Windows and right-click it. Turn off the items you do not want to display. Mine is generally set up like this:

<img src=".\images\TaskBar.png" alt="Taskbar" style="zoom:75%;" />

Click `Search (H)`, and I choose to hide the search icon because it is not very useful. I usually use `Win + Space` for search instead. Click `News and interests (N)`, and I choose to turn it off. Then click `Taskbar settings (T)` at the bottom.

Under `Notification area` --> `Turn system icons on or off`, choose the icons you want to keep.

In the `News and interests` and `People` section, turn them off.

As for the apps in the lower-left corner, set them however you like.

## System Settings

Open Settings (`Win + I`).

1. Remove apps

Find `Apps` and uninstall anything you do not want or do not like. Generally speaking, if you are using an official Microsoft installation, there will not be that many extra apps.

2. Privacy settings

Go to `Privacy` --> `General`, and turn off all tracking options.

Turn off `Contacts` and `Phone calls`.

Under `Background apps`, disable software you do not use often.

3. Start menu settings

Press the `Win` key to open the Start menu, select the Settings icon, right-click it, and choose `Personalize`. There you can choose which icons appear on the Start menu.

![start-menu-setting](./resources/images/start-menu-setting.png)

Personally, I only keep the Settings option.

![start-menu](./resources/images/start-menu-setting-1.png)

## File Explorer Settings

`View` --> `Options` --> `Open File Explorer to:` `This PC`

![filesystem](./resources/images/filesystem-setting-0.png)

At the same time, I disable `Show frequently used folders` and `Show recently used files` in Quick Access, and I also unpin the four default pinned items in Quick Access.

![filesystem](./resources/images/filesystem-setting-1.png)

For the five system folders on the left side, `Videos`, `Documents`, `Downloads`, `Music`, and `Pictures`, change their paths to drive `E:`.

Create five folders with the same names on drive `E:`, then select `Videos` on the left side, right-click --> `Properties` --> `Location` --> `Move`, and choose the newly created folder with the same name.

1. About Quick Access

   I usually use it like this: in the `Data` drive, create a frequently used folder, such as `English Vocabulary Notes`, then pin it to Quick Access and hide it in the `Data` drive to keep things tidy.

   As mentioned above, I hide the `Downloads`, `Videos`, `Pictures`, and `Music` folders that were moved to the `Data` drive. This way, I can access them directly through `This PC` in the sidebar without going into the `Data` drive.

# Default Apps

Change PDF files to open with Edge by default: [How to change PDF default opening to Edge_win10 PDF always opens with Edge - CSDN Blog](https://blog.csdn.net/nofall_bird/article/details/138244710)

# Activate Windows

[[WeiLingWei]-Windows/Office Full Activation Tutorial-KMS Online Activation-KMS Activation Server-Windows 11 Permanent Activation with One Command-Windows 10 Permanent Activation with One Command (jihuowin.com)](https://jihuowin.com/index.php)

Refer to this link.

# Startup Programs

In this path:

```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
```

you can place programs that should start when Windows 10 boots. You can also write your own programs and put shortcuts to them here.

# Reference

[^Bilibili]: [Settings You Should Change Immediately After Getting a New Computer!_bilibili](https://www.bilibili.com/video/BV1am4y1R7pi/?spm_id_from=333.880.my_history.page.click&vd_source=617c4a2b4e326fc6b6269aada0d25986)
