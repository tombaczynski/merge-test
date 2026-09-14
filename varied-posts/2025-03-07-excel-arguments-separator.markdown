---
layout: post
title:  "Excel arguments separator"
date:   2025-03-07 08:19 +0100
categories: Excel
---

Jak to jest? Wczoraj kilkadziesiąt minut szukałem rozwiązania, a wstałem rano i zaraz znalazłem rozwiązanie.

Okazuje się bowiem, że moim Excelu, który jest po angielsku, separatorem w formułach pomiędzy argumentami jest średnik.

`=OR(AND(OR($L3="width";$L3="height");ISNUMBER($M3);INT($M3)=$M3;$M3>0); AND($L3="none";OR($M3=0;ISBLANK($M3))))`
