<template>
    <div id="_ejemplo_" class="grafico" style="height:400px"></div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

export default {
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            colors: ["#67b7dc", "#6794dc", "#6771dc", "#8067dc", "#a367dc", "#c767dc", "#dc67ce", "#dc67ab", "#dc6788", "#dc6967", "#dc8c67", "#dcaf67", "#dcd267", "#c3dc67", "#a0dc67", "#7ddc67", "#67dc75", "#67dc98", "#67dcbb", "#67dadc"],
        }
    },
    methods: {
        createChart: function(){
            am4core.useTheme(am4themes_animated);
            var colorSet = new am4core.ColorSet();
            colorSet.list = this.colors.map(col => new am4core.color(col));


            var chart = am4core.create("_ejemplo_", am4charts.XYChart);
            chart.colors = colorSet;
            chart.data = [{"country": "USA","visits": 2025}, {"country": "China","visits": 1882}, {"country": "Japan","visits": 1809}, {"country": "Germany","visits": 1322}, {"country": "UK","visits": 1122}, {"country": "France","visits": 1114}, {"country": "India","visits": 984}, {"country": "Spain","visits": 711}, {"country": "Netherlands","visits": 665}, {"country": "Russia","visits": 580}, {"country": "South Korea","visits": 443}, {"country": "Canada","visits": 441}];
            chart.padding(40, 40, 40, 40);

            var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
            categoryAxis.renderer.grid.template.location = 0;
            categoryAxis.dataFields.category = "country";
            categoryAxis.renderer.minGridDistance = 60;
            //categoryAxis.renderer.inversed = true;
            categoryAxis.renderer.grid.template.disabled = true;

            var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
            valueAxis.min = 0;
            valueAxis.extraMax = 0.1;
            //valueAxis.rangeChangeEasing = am4core.ease.linear;
            //valueAxis.rangeChangeDuration = 1500;

            var series = chart.series.push(new am4charts.ColumnSeries());
            series.dataFields.categoryX = "country";
            series.dataFields.valueY = "visits";
            series.tooltipText = "{valueY.value}"
            series.columns.template.strokeOpacity = 0;
            series.columns.template.column.cornerRadiusTopRight = 10;
            series.columns.template.column.cornerRadiusTopLeft = 10;
            //series.interpolationDuration = 1500;
            //series.interpolationEasing = am4core.ease.linear;
            var labelBullet = series.bullets.push(new am4charts.LabelBullet());
            labelBullet.label.verticalCenter = "bottom";
            labelBullet.label.dy = -10;
            labelBullet.label.text = "{values.valueY.workingValue.formatNumber('#.')}";

            chart.zoomOutButton.disabled = true;

            // as by default columns of the same series are of the same color, we add adapter which takes colors from chart.colors color set
            series.columns.template.adapter.add("fill", function (fill, target) {
            return chart.colors.getIndex(target.dataItem.index);
            });

            /*setInterval(function () {
                am4core.array.each(chart.data, function (item) {
                item.visits += Math.round(Math.random() * 200 - 100);
                item.visits = Math.abs(item.visits);
                })
                chart.invalidateRawData();
            }, 2000)*/

            categoryAxis.sortBySeries = series;
        },
    },
    mounted(){
        this.createChart();
    }
}
</script>