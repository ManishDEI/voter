var ctx = document.getElementById("voterDistribution");


var mixedChart = new Chart(ctx, {
    type: 'bar',
    data: {
        //labels: ['Small', 'Medium', 'Large', 'X-Large'],
        labels: bar_label,
        datasets: [{
            //label: bar_label,
            //data: [80, 20, 30, 40],
            backgroundColor: "rgba(2,117,216,1)",
            //borderColor: "rgba(2,117,216,1)",
            data: bar_data,
        }],
        
    },

    options:{
        scales:{
            xAxes: [{
                time: {
                    unit: 'State'
                },
                gridLines: {
                    display: false
                },
            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    maxTicksLimit: 6
                },
                gridLines: {
                    display: true
                }
            }],
        },
        legend: {
            display: false
        }
    }
    
});