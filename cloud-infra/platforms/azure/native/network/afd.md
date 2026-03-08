# AFD pricing

[Pricing - Front Door | Microsoft Azure](https://azure.microsoft.com/en-us/pricing/details/frontdoor/)



# AFD configuration

[Add a new endpoint with Front Door manager - Azure Front Door | Microsoft Learn](https://learn.microsoft.com/en-us/azure/frontdoor/how-to-configure-endpoints)



# Standard VS Premium

standard AFD 和 Premium AFD 的区别除了在价格之上，还有一些地方存在区别

## waf

首先 standard afd waf 和 premium afd waf 是不同的 2 个 sku

然后 standard afd waf 不能使用 managed rule ,也就是不能使用 owasp rule, 只有 premium 才可以使用

> tmd, azure 真是太会赚钱了

