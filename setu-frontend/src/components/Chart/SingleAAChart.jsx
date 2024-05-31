"use client";

import React from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

// Get a random number between min and max
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Render a single trends chart for a particular AA
 * @param {String} aaName The AA Name
 * @param {Array} aaData All AA docs
 * @param {Boolean} addMockData whether to add mock data for this chart
 */
function SingleAAChart({ aaName, aaData, addMockData }) {
    let labels = [];

    let naDataPoints = [];
    let liveDataPoints = [];
    let testDataPoints = [];

    // Add mock data to the labels and data points
    if (addMockData) {
        for (let i = 0; i < 3; i++) {
            labels.push(`0${i + 1}-01`);
            naDataPoints.push(getRandomInt(0, 120));
            liveDataPoints.push(getRandomInt(0, 120));
            testDataPoints.push(getRandomInt(0, 120));
        }
    }

    labels = [...labels, ...aaData.map((el) => 
        // remove the year("-YYYY") from the date
        el.date.slice(0, -5)
    )];

    // Prepare data points for the AA
    for (const eachDayAaData of aaData) {
        const { na_count, live_count, testing_count } =
            eachDayAaData.aas_data[aaName];
        naDataPoints.push(na_count);
        liveDataPoints.push(live_count);
        testDataPoints.push(testing_count);
    }


    // Line Animations
    const animations = {
        tension: {
            duration: 2000,
            easing: "linear",
            from: 0.5,
            to: 0.3,
            loop: true,
        },
    };

    // Line tension
    const tension = 0.5;

    const data = {
        labels,
        datasets: [
            // Live data set
            {
                label: "Live",
                data: liveDataPoints,
                borderColor: "#00FF00",
                backgroundColor: "#00FF0070",
                tension,
                animations,
            },
            // Testing dataset
            {
                label: "Testing",
                data: testDataPoints,
                borderColor: "#00BFFF",
                backgroundColor: "#00BFFF70",
                tension,
                animations,
            },
            // N/A dataset
            {
                label: "N/A",
                data: naDataPoints,
                borderColor: "#FF00FF",
                backgroundColor: "#FF00FF70",
                tension,
                animations,
            },
        ],
    };

    // Chart options
    const options = {
        responsive: true,
        layout: {
            // Apply 20px padding to all sides
            padding: 20,
        },

        plugins: {
            legend: {
                position: "bottom",
                labels: {
                    font: {
                        size: 16,
                    },
                    padding: 20,
                },
            },
            title: {
                align: "start",
                display: true,
                text: aaName,
                color: "#1e1e1e",
                padding: {
                    bottom: 20,
                },
                font: {
                    size: 22,
                    weight: "600",
                },
            },
        },
    };

    return (
        <div
            className="single-chart-container"
            style={{

                // use a 2 column layout if labels are less than 5
                // else use a single column layout, to have more space to display points
                width: labels.length <= 5 ? "49%" : "90%",
            }}
        >
            {/* The line chart */}
            <Line options={options} data={data} />
        </div>
    );
}

export default SingleAAChart;
