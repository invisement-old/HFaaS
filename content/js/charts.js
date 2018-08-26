///*
https://fred.stlouisfed.org/series/UMCSENT
https://fred.stlouisfed.org/series/A006RE1Q156NBEA

*/////



/////////           FRED data fetch and chart       /////
myFredApiKey = "88b9092ad3db013e454ea78d5a1084c9"
high_yield_series = "BAMLH0A0HYM2EY"
treasury_spread_series = "T10Y2Y"
fred_endpoint = "http://api.stlouisfed.org/fred/series/observations"
fred_file_type = "json"

// https://api.stlouisfed.org/fred/series/observations?series_id=T10Y2Y&api_key=88b9092ad3db013e454ea78d5a1084c9&file_type=json

function chart_treasury_spread (location) {
    //    url = fred_endpoint + "?series_id=" + treasury_spread_series + "&api_key=" + myFredApiKey + "&file_type=" + fred_file_type
    fetch("http://127.0.0.1:8887/fred.json")
    .then(res => res.json())
    .then(function(input){
        timeSeriesChartOption['dataset']['source'] = input['observations'];
        treasurySpreadChart.setOption(timeSeriesChartOption);
        
        // function quantile (data, past, history)
        data = input['observations'].map(x => Number(x['value']))
        data = data.slice(-255*30) // past 30 years
        var current_value = data.slice(-1)[0];
        var past_value = data.slice(-60)[0];
        data.sort(function(x,y){
            return x-y
        });
        current_quantile = data.indexOf(current_value)/data.length;
        past_quantile = data.indexOf(past_value)/data.length;
        return [current_quantile, past_quantile]

        treasurySpreadChart = echarts.init(document.getElementById(location));
        timeSeriesChartOption['title'] = {
            left: 'center', 
            text: 'Economic Risk Spread', 
            subtext: '10 year treasury yield minus 2 year treasury yield'
        };
    
        console.log(data.slice(10), idx/data.length);
    });

}


function chart_fred (location, fred_series, historical_years, quantile_indexes) {
    /* fetch fred series, grab observations, draw chart in location, calc and return quantiles */
    historical_years = historical_years || 30*255 // in years
    quatile_indexes = quantile_indexes || [0, 60] // return the quatile of values from data with these indexes
    url = fred_endpoint + "?series_id=" + fred_series + "&api_key=" + myFredApiKey + "&file_type=" + fred_file_type
    fetch("http://127.0.0.1:8887/fred.json")
    .then(res => res.json())
    .then(function(input){
        timeSeriesChartOption['dataset']['source'] = input['observations'];
        treasurySpreadChart.setOption(timeSeriesChartOption);
        numbers = input['observations'].map(x => Number(x['value']))

        treasurySpreadChart = echarts.init(document.getElementById(location));
        timeSeriesChartOption['title'] = {
            left: 'center', 
            text: 'Economic Risk Spread', 
            subtext: '10 year treasury yield minus 2 year treasury yield'
        };
    

}

function calculate_quantiles (numbers, value_indexes, length_of_data_to_use) {
    value_indexes = value_indexes || [0, 60]
    length_of_data_to_use = length_of_data_to_use || 255*30 // default to 30 years daily data
    //data = input['observations'].map(x => Number(x['value']))
    numbers = numbers.slice(-length_of_data_to_use) // grab only past 30 years
    values = quantile_indexes.map(index => numbers.slice(numbers.length-index)[0]) // grab values from end of data
    //var current_value = data.slice(-1)[0];
    //var past_value = data.slice(-60)[0];
    numbers.sort(function(x,y){
        return x-y
    });
    quantiles = values.map(value => data.indexOf(value)/data.length)
    //current_quantile = data.indexOf(current_value)/data.length;
    //past_quantile = data.indexOf(past_value)/data.length;
    return quantiles
}

/////////       Risk Gauge      ///////////

function chart_risk_gauge (div, financial_risks, economic_risks, perceived_risks) {
    var riskGauge = echarts.init(document.getElementById(div));
    riskGauge_option.series[0].data = [{value: financial_risks[0], name: 'Financial Risk'}, {value: financial_risks[1], name:'last year financial risk', pointer: {width: 2}}] // set values for financial risk gauge
    riskGauge_option.series[1].data = [{value: economic_risks[0], name: 'Economic Risk'}, {value: economic_risks[1], name:'last year economic risk', pointer: {width: 2}}] //set values for economic risk gauge
    riskGauge_option.series[2].data = [{value: perceived_risks[0], name: 'Perceived Risk'}, {value: perceived_risks[1], name:'last year perceived risk', pointer: {width: 2}}] //set values for perceived risk gauge
    riskGauge.setOption(riskGauge_option, true);
}

riskGauge_option = {
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
            magicType: {type: ['line', 'bar']},
            dataView: {readOnly: false}
        }
    },
    dataset: {
        dimensions: ['date', 'value'],
    },
    xAxis: {type: 'category', scale: true},
    yAxis: {type: 'value', scale: true, axisLabel: {formatter: '{value}%'}},
    series: [{
            type: 'bar', 
            smooth: true, 
            symbol: 'none', 
            sampling: 'average', 
            ///////////// HERE
            // *************************


            markLine: {data:[{type: 'average'}, {value: 20, valueIndex: 1, xAxis: '2018-04-10', yAxis: 2.0}]},
            markPoint: {data: [{name: 'Current Risk', xAxis: '2018-04-10', yAxis: 2.0}]},
            itemStyle: {emphasis: {borderColor: 'blue', borderWidth: 3}}
        }],
    dataZoom: [{startValue: '1985-01-01'}],
};



/////////           END         ///////
