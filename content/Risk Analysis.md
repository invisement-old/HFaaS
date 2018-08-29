---
title: "Market Risk Dashboard"
date: 2018-08-18
tags: ["Blog", "Market Analysis", "Market Risk", "Risk Analysis"]
card: '<figure id="Risk Gauge" style="width: auto; height:400px;">'

---

inVisement deploys a very quantitative approach to create Market Risk Dashboard, 
which is based on 3 levels, each measuring a fundamental risk factor based on past 30 years of historical data:

- Microeconomic Condition: Corporate Financial Risk
    - Measure: High Yield Bond Spread
- Macroeconomic Condition: Monetary Policies
    - Measure: Treasury Yield Spread
- Investors Sentiment: Perceived Risk
    - Measure: Consumer Sentiment 

___
## Corporate Financial Risk
The corporate financial risk is a major risk factor that can be captured well by High Yield Bond Spread. It shows how much the lenders ask for premium when deciding to buy junk (or low credit) corporate bonds. 

<figure id="High Yield Spread" style="width: auto; height:400px;"> </figure>

___
## Economic Risk
Inflation and economic cycles are among the primary causes of the market turbulence. The federal reserve (and the market) carefully watch the economic conditions such as inflation, economic growth, and unemployment rate to take appropriate monetary policies and decisions. 

The yield spread between 10 year Treasury and 2 year Treasury captures captures the direction of the monetary policy to expand (upward spread) or to contradict (downward spread). When the economic prospect is cloudy, the spread starts soaring up, it is time to sell stocks and hold on to your cash.

<figure id="Treasury Yield Spread" style="width: auto; height:400px;"> </figure>

___
## Perceived Risk 
Perceived risk depends on citizens' sentiment about the stock prices and the economic condition. One of the best graphs that captures economic condition sentiment is a poll by University of Michigan about the Consumer Sentiment that has been around for a long time:

<figure id="Consumer Sentiment" style="width: auto; height:400px;"> </figure>

___
<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/4.1.0/echarts-en.min.js" integrity="sha256-x8R4YOgRkrX/cMbupOzglWi/gSM/WD8bfFHrE+r5TPM=" crossorigin="anonymous"></script>

<script src="/js/charts.js"></script>

<script> chart_risks_page(); </script>

<!--
To do:
- All data from FRED must be downloaded to your google storage bucket
- Add legend to time series and stack to magic 
-->


