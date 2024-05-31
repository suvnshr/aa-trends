"use client";

import axios from "axios";
import React, { useEffect, useState } from "react";
import SingleAAChart from "./SingleAAChart";

import config from "@/config/config.json";

/**
 * Chart container in which all the charts are rendered
 * @param {Array} mockData Populate with mock data
 */
function AAChartContainer({mockData = null}) {

    // AA docs
    const [aaData, setAaData] = useState(mockData ?? null);
    const [error, setError] = useState(false);

    // Mock data
    const [addMockData, setAddMockData] = useState(false);

    useEffect(() => {
        // Fetch aa docs
        axios
            .get(config.urls.FETCH_AA)
            .then((res) => {
                let __aaData = res.data?.data ?? [];
                setAaData(__aaData);

                // If the fetched data's length is less than 3
                // then display mock data too
                if (__aaData.length < config.mock.MIN_LENGTH_TO_DISPLAY) {
                    setAddMockData(true);
                } else {
                    setAddMockData(false);
                }
            })
            .catch((e) => setError(true));
    }, []);

    // Loading
    if (aaData === null) {
        return <p>Loading...</p>;
    }

    // Error
    if (error) {
        return <p>Error occured while fetching data</p>;
    }

    // Get the different AA names from the first doc
    let aaNames = Object.keys(aaData?.[0]?.aas_data ?? {});

    // If no docs were fetched, then use the mock names to display data
    aaNames = aaNames.length ? aaNames : config.mock.aaNames;

    return (
        <div data-testid="chart-container-id" className="chart-container">

            {/* Loop over each aa name and render it's trend chart */}
            {aaNames.map((aaName) => (
                <SingleAAChart
                    key={`${aaName}-chart`}
                    aaName={aaName}
                    aaData={aaData}
                    addMockData={addMockData}
                />
            ))}
        </div>
    );
}

export default AAChartContainer;
