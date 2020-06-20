Plotly.d3.csv("public_CPA01.csv", function (row1) {
    Plotly.d3.csv("public_CMH24.csv", function (row2) {
        Plotly.d3.csv("public_CMH04.csv", function (row3) {
            Plotly.d3.csv("public_CMH01.csv", function (row4) {
                        function unpack(row1, key) {
                            return row1.map(function (row) { return row[key]; });
                        }
                        function unpack(row2, key) {
                            return row2.map(function (row) { return row[key]; });
                        }
                        function unpack(row3, key) {
                            return row3.map(function (row) { return row[key]; });
                        }
                        function unpack(row4, key) {
                            return row4.map(function (row) { return row[key]; });
                        }

                        var trace1 = {
                            type: "scatter",
                            mode: "lines",
                            name: 'Painter Creek (CPA01)',
                            x: unpack(row1, 'rounded_time'),
                            y: unpack(row1, 'level_ft'),
                            line: { color: '00b8ff' }
                        };
                        var trace2 = {
                            type: "scatter",
                            mode: "lines",
                            name: 'Minnehaha Creek (CMH24)',
                            x: unpack(row2, 'rounded_time'),
                            y: unpack(row2, 'level_ft'),
                            line: { color: '008ecc' }
                        };

                        var trace3 = {
                            type: "scatter",
                            mode: "lines",
                            name: 'Minnehaha Creek (CMH04)',
                            x: unpack(row3, 'rounded_time'),
                            y: unpack(row3, 'level_ft'),
                            line: { color: '1034a6' }
                        };

                        var trace4 = {
                            type: "scatter",
                            mode: "lines",
                            name: 'Minnehaha Creek (CMH01)',
                            x: unpack(row4, 'rounded_time'),
                            y: unpack(row4, 'level_ft'),
                            line: { color: '1034a6' }
                        };

                        var data = [trace1, trace2, trace3, trace4];
                        var layout = {
                            title: 'Stream Water Level',
                            yaxis: {
                                title: {
                                    text: 'Stream Elevation (ft)'
                                }
                            }
                        };
                        Plotly.newPlot('level', data, layout, {});
                    })
                })
            })
        })