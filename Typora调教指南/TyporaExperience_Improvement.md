# Typora 修改快捷键

According to this document: [Shortcut Keys - Typora Support](https://support.typora.io/Shortcut-Keys/#change-shortcut-keys)

we can change Shortcut Keys through modified the `conf.user.json` file

and here is my changed file

```json
/** For advanced users. */
{
  "defaultFontFamily": {
    "standard": null, //String - Defaults to "Times New Roman".
    "serif": null, // String - Defaults to "Times New Roman".
    "sansSerif": null, // String - Defaults to "Arial".
    "monospace": null // String - Defaults to "Courier New".
  },
  "autoHideMenuBar": false, //Boolean - Auto hide the menu bar unless the `Alt` key is pressed. Default is false.

  // Array - Search Service user can access from context menu after a range of text is selected. Each item is formatted as [caption, url]
  "searchService": [
    ["Search with Google", "https://google.com/search?q=%s"]
  ],

  // Custom key binding, which will override the default ones.
  // see https://support.typora.io/Shortcut-Keys/#windows--linux for detail
  "keyBinding": {
    // for example: 
    // "Always on Top": "Ctrl+Shift+P"
    // All other options are the menu items 'text label' displayed from each typora menu

    // add by hanjie-chen in 2024-08-19
    "Highlight": "Ctrl+Shift+H",
    "Comment": "Ctrl+/",
    "Source Code Mode": "Ctrl+Shift+/",
    "Code Fences": "Ctrl+`",
    "Delete Line / Sentence" : "Ctrl+Shift+K",
    "Open Folder" : "Ctrl+Shift+O"
  },

  "monocolorEmoji": false, //default false. Only work for Windows
  "maxFetchCountOnFileList": 500,
  "flags": [] // default [], append Chrome launch flags, e.g: [["disable-gpu"], ["host-rules", "MAP * 127.0.0.1"]]
}
```

I change the `Comment` and `delete Line / Sentence` function shortcut, also change the shortcut which have conflcts with these.



# How to cancel the exist shortcut of the Typora

After I wirte an Email to the Typora team hi@typora.io, and I get the resolution:

You can unbind like this:

"Code Fences": ""

Then Code Fences is unbind with shortcut keys.
