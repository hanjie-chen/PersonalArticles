# Windows Powershell Command

## Dir Command

1. to see all file of the folder

   ```powershell
   dir -Force
   ```

   <img src="./images/dir-compare.png" alt="compare of two kind of command" style="zoom:70%;" />

## New-Item Command

1. create new folder

   ```powershell
   New-Item -ItemType Directory -Name "Foldername"
   ```

   ![create new folder](./images/create-folder.png)

## Nslookup Command

trun the domain name into IP address

Now I use the nslookup command like that `nslookup baidu.com`, and here is the feedback:
```
服务器:  public1.alidns.com
Address:  223.5.5.5

非权威应答:
名称:    baidu.com
Addresses:  39.156.66.10
 110.242.68.66
```
But when I try to use 39.156.66.10 and  110.242.68.66 to visit baidu.com, it can't work. Why ? Do the way I use nslookup is wrong ?

Answer:

The `nslookup` command you used is correct and it provided you with the IP addresses associated with the domain name `baidu.com`. However, there could be several reasons why you are unable to access the website using those IP addresses. 

One possibility is that the website is hosted on a shared server and the IP addresses you obtained are not unique to the website. Another possibility is that the website is using a content delivery network (CDN) or load balancer, which means that the IP addresses associated with the website may change frequently.

In general, it's recommended to access websites using their domain names rather than IP addresses, as this allows for more flexibility in case the IP address changes.