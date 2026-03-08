# Azure public ip

Internet 到 VM public ip 的流量会做一个 DNAT，在 VM 上面只能看到 destination 是 private ip

文档 [Associate a public IP address to a virtual machine | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/associate-public-ip-address-vm?tabs=azure-portal#allow-network-traffic-to-the-vm) 提到

> Although network security groups filter traffic to the private IP address of the network interface, **<u>*after inbound internet traffic arrives at the public IP address, Azure translates the public address to the private IP address.*</u>** 



所以如果想要在 nsg inbound 中实现 allow/block 某个拥有 public ip 的 resource 的 traffic，那么在 nsg inbound rule 中不能写 Azure public ip, 而是它的 private ip, 在 VM 上面看到的包的 destination 也是 private ip



在这个 microsoft Q&A 中也有提及 [Is there a way to assign a Public IP to the network interface of a Azure VM without NAT to a private IP? - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1663911/is-there-a-way-to-assign-a-public-ip-to-the-networ)