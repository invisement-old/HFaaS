---
title: "Market Risk Dashboard"
date: 2018-08-18
tags: ["Blog", "Market Analysis", "Market Risk", "Risk Analysis"]
card: '<figure id="risk_gauge" style="width: 700px; height:400px;"> </figure><figcaption>Thick Hand: Current <br> Thin Hand: Last Quarter </figcaption>'

---

<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/4.1.0/echarts-en.min.js" integrity="sha256-x8R4YOgRkrX/cMbupOzglWi/gSM/WD8bfFHrE+r5TPM=" crossorigin="anonymous"></script>
<script src="/js/charts.js"></script>

<script> set_risk_gauge("risk_gauge", [31, 26], [23, 29], [66, 54]);</script>

inVisement deploys a very quantitative approach to create Market Risk Dashboard, 
which is based on 3 levels, each measuring a fundamental risk factor based on past 30 years of historical data:

- Microeconomic Condition: Corporate Financial Risk
    - Measure: High Yield Bond Spread
- Macroeconomic Condition: Monetary Policies
    - Measure: 10-2 Treasury Yield Spread
- Investors Sentiment: Perceived Risk
    - Measure: Bear-Bull Sentiment Spread


## Corporate Financial Risk
The corporate financial risk is a major risk factor that can be captured well by High Yield Bond Spread. It shows how much the lenders ask for premium when deciding to buy junk (or low credit) corporate bonds. 

<div class="embed-container"><iframe src="//fred.stlouisfed.org/graph/graph-landing.php?g=kTTg&width=100%" scrolling="no" frameborder="0" style="overflow:hidden; allowTransparency="true"></iframe></div><script src="https://fred.stlouisfed.org/graph/js/embed.js" type="text/javascript"></script>

Right now, the corporate financial risk is very low.

**August 2018 Financial Risk 20%**

## Economic Risk
Inflation and economic cycles are among the primary causes of the market turbulence. The federal reserve (and the market) carefully watch the economic conditions such as inflation, economic growth, and unemployment rate to take appropriate monetary policies and decisions. The yield spread between 10 year Treasury and 2 year Treasury captures captures the direction of the monetary policy to expand (upward spread) or to contradict (downward spread). When the economic prospect is cloudy, the spread starts soaring up, it is time to sell stocks and hold on to your cash.

<div class="embed-container"><iframe src="//fred.stlouisfed.org/graph/graph-landing.php?g=kTTb&width=100%" scrolling="no" frameborder="0" style="overflow:hidden; allowTransparency="true"></iframe></div><script src="https://fred.stlouisfed.org/graph/js/embed.js" type="text/javascript"></script>


Right now, the 10-year Treasury is mostly flat while the 10-2 spread is decreasing, which is a boom cycle indicator.

**August 2018 Economic Risk: 40%**

## Perceived Risk 
Perceived risk depends on investors sentiment about the stock prices and the economic condition. One of the best graphs that captures investors sentiment is how often they search (in google) for bear market vs bull market. The below graph shows this bear-bull spread:

<object width="100%" height="400" type="text/html" data="/htmls/bull-bear-trend-graph.html"></object>

The graph shows the investors are moderately worried about the stock prices or economic condition.

**August Investors Risk: Medium 70%** 

----

# Appendix: Potential Risk Factors
The US economy is growing fast and the unemployment rate is very low, however there are crawling risks that might turn the current bull into a bear:

- **Higher Interest Rates**
The Fed is constantly raising the prime rates to damper crawling inflation.

    - Despite the Federal Reserve's concern abut rising inflation, which currently sits around 2%, this is quite low for a boom economic cycle.

    - The Fed's ability to manipulate interest rates (through higher prime rates) is often exaggerated. The past two months show the market interest rates were mainly stagnant. This is similar to the late 90s when the Federal Reserve was not able to harness the financial expansion.

    - Despite the higher prime rates, consumers keep spending, banks keep lending, stocks keep growing, and employers keep hiring; showing the market's resilience to higher prime rates.

- **Slowing Real Estate**. One of the biggest concerns among market analysts is the decline in homes sold over the past six months. The higher mortgage rates, caused by the higher prime rate, has decreased the home buyers' affordability. 

- **Trade Wars**
The White House, with its **mercantilism** approach, is too optimistic about the US' ability to close the trade gap. The White House's "easy war to win" is a lose-lose game to everyone.

    - Mercantilism is a popular misconception about how the economy works. The US trade deficit is natural and is a privilege to the US. It is caused by the "Capital Account Surplus." The US is the world's capital market: while the US economy accounts for less than 20% of the world's economy, the US capital market is about 50% of the world's capital market. Therefore, it is natural (and healthy) to see the US attracting a tremendous capital inflow from the rest of the world, which means the US would have a huge trade deficit (excess imports over exports.) The US is the world's Manhattan.

    - Trade policies such as higher tariff would result in **Stronger US Dollar** (the monetary substitution effect) and **Economic Inefficiencies** (the real economy substitution effect). Nonetheless, the White House has shown flexibility in reaching deals with its' neighbors and the EU. The only big concern is the US trade war with China, which seems to be an unfortunate popular policy. The market is strong enough to overcome this problem, especially through the stronger dollar and weaker Chinese Yuan.

- **Skill Shortage**
The populist wrath against immigration, accompanied with low unemployment, might cause lack of skilled workers to fill the jobs that an economy needs when growing faster than usual. This is one of the biggest threats for sustainability of the high economic growth.

<!--
To do:
- Make tabs for risks
- Connect risk numbers to graph for auto update
    - make numbers like histogram and find current number as quantile for risk
-->
