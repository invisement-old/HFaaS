


/////////       Risk Gauge      ///////////

function set_risk_gauge (div, financial_risks, economic_risks, perceived_risks) {
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
/////////           END         ///////
