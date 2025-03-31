如果 application gateway 处于 failed 状态，可以在 Properties 中看到

首先可以尝试使用 get-set 命令重置 apg

[Set-AzApplicationGateway (Az.Network) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/az.network/set-azapplicationgateway?view=azps-13.3.0)

有时候可能会有效果，特别是针对于之前还在 work 的 application gateway 来说