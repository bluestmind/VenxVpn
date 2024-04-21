function getChartColorsArray(chartClass) {
    var colors = $(chartClass).attr('data-colors');
    var colors = JSON.parse(colors);
    return colors.map(function(value){
        var newValue = value.replace(' ', '');
        if(newValue.indexOf('--') != -1) {
            var color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
            if(color) return color;
        } else {
            return newValue;
        }
    });
}

function getChartDays(chartClass) {
    var days = $(chartClass).attr('data-days');
    console.log("days",days)
    return JSON.parse(days);
}
document.addEventListener("DOMContentLoaded", function() {
    // Select all elements with the class 'invested-overview'
    var chartContainers = document.querySelectorAll(".apex-charts");

    // Iterate over each chart container
    chartContainers.forEach(function(container) {
        var radialchartColors = getChartColorsArray(container);
        var days = getChartDays(container);
        var options1 = {
            chart: {
                height: 270,
                type: 'radialBar',
                offsetY: -10
            },
            plotOptions: {
                radialBar: {
                    startAngle: -130,
                    endAngle: 130,
                    dataLabels: {
                        name: {
                            show: false
                        },
                        value: {
                            offsetY: 10,
                            fontSize: '18px',
                            color: undefined,
                            formatter: function (val) {
                                return val + " days";
                            }
                        }
                    }
                }
            },
            colors: [radialchartColors[0]],
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'dark',
                    type: 'horizontal',
                    gradientToColors: [radialchartColors[1]],
                    shadeIntensity: 0.15,
                    inverseColors: false,
                    opacityFrom: 1,
                    opacityTo: 1,
                    stops: [10, 20]
                }
            },
            stroke: {
                dashArray: 4
            },
            legend: {
                show: false
            },
            series: [days],
            labels: ['Series A']
        };

        var chart = new ApexCharts(container, options1);
        chart.render();
    });
});

var mixLineDom = document.getElementById("mix-line-bar");
var mixLineChart = echarts.init(mixLineDom);

var mixlinebarColors = ['#2ab57d', '#5156be', '#fd625e'];

var option = {
    // Setup grid
    grid: {
        left: '1%',
        right: '0%',
        bottom: '0%',
        top: '4%',
        containLabel: true
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        }
    },
    color: mixlinebarColors,
    legend: {
        top: '0',
        data: ['Number of users', 'Total Profit', 'Average Profit'],
        textStyle: { color: '#858d98' }
    },
    xAxis: [
        {
            type: 'category',
            data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            axisPointer: {
                type: 'shadow'
            },
            axisLine: {
                lineStyle: {
                    color: '#858d98'
                },
            }
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: 'Profit amount',
            min: 0,
            max: 250,
            interval: 50,
            axisLine: {
                lineStyle: {
                    color: '#858d98'
                },
            },
            splitLine: {
                lineStyle: {
                    color: "rgba(133, 141, 152, 0.1)"
                }
            },
            axisLabel: {
                formatter: '{value}'
            }
        },
        {
            type: 'value',
            name: 'Temperature',
            min: 0,
            max: 25,
            interval: 5,
            axisLine: {
                lineStyle: {
                    color: '#858d98'
                },
            },
            splitLine: {
                lineStyle: {
                    color: "rgba(133, 141, 152, 0.1)"
                }
            },
            axisLabel: {
                formatter: '{value} Trx'
            }
        }
    ],
    series: [
        {
            name: 'Number of users',
            type: 'bar',
            barWidth: '50%',
            data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2]
        },
        {
            name: 'Total Profit',
            type: 'bar',
            barWidth: '50%',
            data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2]
        },
        {
            name: 'Average Profit',
            type: 'line',
            yAxisIndex: 1,
            data: [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4]
        }
    ]
};

if (option && typeof option === "object") {
    mixLineChart.setOption(option, true);
}