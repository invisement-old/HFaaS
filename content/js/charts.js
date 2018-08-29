
/// attention: chart name and chart location id must match

fred_series = {
    key: "88b9092ad3db013e454ea78d5a1084c9",
    endpoint: "https://api.stlouisfed.org/fred/series/observations",
    file_type: "json",
    "High Yield Spread": {
        id: "BAMLH0A0HYM2EY",
        subtitle: "10 year treasury yield minus 2 year treasury yield",
    },
    "Treasury Yield Spread": {
        id: "T10Y2Y",
        subtitle: "Risky Corporate Bond Yield minus Treasury Bond Yield"
    },
    "Consumer Sentiment": {
        id: "UMCSENT",
        subtitle: "Consumer Sentiment Index (1966:Q1=100)"
    },
    "Investment to GDP": {
        id: "A006RE1Q156NBEA",
        subtitle: "Share of Investment from GDP in Percent"
    }
}


function chart_risks_page () {
    indexes = [1, 60]
    historical_length = 255*30

    economic_risks = chart_fred ("Treasury Yield Spread")
    .then(data => data['value'].slice(-historical_length))
    .then(numbers => quantiles (indexes, numbers))

    financial_risks = chart_fred ("High Yield Spread")
    .then(data => data['value'].slice(-historical_length))
    .then(numbers => quantiles (indexes, numbers))

    perceived_risks = chart_fred ("Consumer Sentiment")
    .then(data => data['value'].slice(-historical_length))
    .then(numbers => quantiles (indexes, numbers))
    .then(risks => risks.map(risk => 1-risk))

    Promise.all([economic_risks, financial_risks, perceived_risks])
    //.then(x => console.log(x[0]))
    .then(risks => chart_gauge ("Risk Gauge", risks[0], risks[1], risks[2]))
}


function chart_fred (name) {
    /* fetch fred series, grab and return observations, draw chart in location */
    // https://api.stlouisfed.org/fred/series/observations?series_id=T10Y2Y&api_key=88b9092ad3db013e454ea78d5a1084c9&file_type=json
    url = fred_series.endpoint + "?series_id=" + fred_series[name].id + "&api_key=" + fred_series.key + "&file_type=" + fred_series.file_type
    url = "http://127.0.0.1:8887/fred.json" // for test purpose only
    return fetch(url, {mode: 'cors'})
    .then(res => res.json())
    .then(function(res){
        observations = res['observations']
        treasurySpreadChart = echarts.init(document.getElementById(name));
        timeSeriesChartOption['title'] = {
            left: 'center', 
            text: name, 
            subtext: fred_series[name].subtitle
        };
        data = {
            date: observations.map(row => row['date']),
            value: observations.map(row => Number(row['value'])),
        }
        timeSeriesChartOption.xAxis.data = data['date']
        timeSeriesChartOption.series[0].data = data['value']
        treasurySpreadChart.setOption(timeSeriesChartOption);
        return data
    });
}

function chart_gauge (name, financial_risks, economic_risks, perceived_risks) {
    var riskGauge = echarts.init(document.getElementById(name));
    gaugeChartOption.series[0].data = [
        {value: parseInt(financial_risks[0]*100), name: 'Financial Risk'}, 
        {value: parseInt(financial_risks[1]*100), name:'last year financial risk', pointer: {width: 2}}
    ] // set values for financial risk gauge
    gaugeChartOption.series[1].data = [
        {value: parseInt(economic_risks[0]*100), name: 'Economic Risk'}, 
        {value: parseInt(economic_risks[1]*100), name:'last year economic risk', pointer: {width: 2}}
    ] //set values for economic risk gauge
    gaugeChartOption.series[2].data = [
        {value: parseInt(perceived_risks[0]*100), name: 'Perceived Risk'}, 
        {value: parseInt(perceived_risks[1]*100), name:'last year perceived risk', pointer: {width: 2}}
    ] //set     qvalues for perceived risk gauge
    riskGauge.setOption(gaugeChartOption, true);
}

gaugeChartOption = {
    title: {text: "Risk Measures", subtext: "Tick Hand: Current Risk\n\nThin Hand: Last Quarter Risk"},
    tooltip: {
        formatter: "{b} : {c}%"
    },
    toolbox: {
        feature: {
            restore: {},
            saveAsImage: {}
        },
    },
    series: [
        {
            name: 'Financial Risk',
            type: 'gauge',
            center: ['50%', '40%'],
            detail: {formatter:'{value}%'},
            axisLine: {            
                lineStyle: {      
                    width: 15
                }
            },
            splitLine: {length: 25},
        },
        {
            name: 'Economic Risk',
            type: 'gauge',
            center: ['20%', '80%'],
            radius: '50%',
            detail: {formatter:'{value}%'},
            splitLine: {length: 10},
            axisLine: {            
                lineStyle: {      
                    width: 3
                }
            },
        },
        {
            name: 'Perceived Risk',
            type: 'gauge',
            center: ['80%', '80%'],
            radius: '50%',
            detail: {formatter:'{value}%'},
            splitLine: {length: 10},
            axisLine: {            
                lineStyle: {      
                    width: 3
                }
            },
        }

    ]
};

timeSeriesChartOption = {
    legend: {data: ['']},
    tooltip: {
        trigger: 'axis',
    },
    toolbox: {
        feature: {
            restore: {},
            saveAsImage: {},
            magicType: {type: ['line', 'bar', 'stack', 'tiled']},
            dataView: {},
        }
    },
    yAxis: {},
    xAxis: {type: 'category', scale: true},
    yAxis: {type: 'value', scale: true, axisLabel: {formatter: '{value}%'}},
    series: [
        {
            type: 'line', 
            smooth: true, 
            symbol: 'none', 
            sampling: 'average', 
            markLine: {data:[{type: 'average'}]},
            itemStyle: {emphasis: {borderColor: 'blue', borderWidth: 2}}
        }
    ],
    dataZoom: [{startValue: '1985-01-01'}],
};

function quantiles (value_indexes, array) {
    value_indexes = value_indexes || [1, 60]
    values = value_indexes.map(index => array.slice(-index)[0]) // grab values from end of data
    array.sort(function(x,y){
        return x-y
    });
    value_quantiles = values.map(value => array.indexOf(value)/array.length)
    return value_quantiles
}


/////////           END         ///////
