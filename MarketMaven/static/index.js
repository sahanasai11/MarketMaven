"use strict";

const ROOTPATH = "http://localhost:5000";
const DEBUG = false;

/**
 * Initialize the preferences form button
 */
function init() {
    submitPreferences();
}

/**
 * Helper function to submit a message input into the form
 */
function submitPreferences() {
    let url = '/'
    id("submit-preferences-btn").addEventListener("click", async (e) => {
        e.preventDefault();

        try {
            let resp = await fetch(url, 
                {   
                    headers : {
                        "Access-Control-Allow-Origin" : "*",
                    },
                    method : "POST", 
                    body : (new FormData(id("preferences-form")))
                });
            resp = checkStatus(resp);
            const data = await resp.json();
            populateIndex(data);
        } catch (err) {
            handleError(err);
        } 
    }); 
}

/**
 * Helper function to populate home page after user presses submit
 * @param {JSON object} data: JSON response after user submission for network 
 * and CAPM info
 */
function populateIndex(data) {
    let network = id("network");
    let capm = id("returns-graph");

    // clear network and capm cards if graph and network currently exists
    network.innerHTML = '';
    capm.innerHTML = '';
    
    let networkImg = gen("img");
    networkImg.src = data["network_img"];
    networkImg.style.width = "90%";
    network.appendChild(networkImg);

    let networkCapmImg = gen("img");
    networkCapmImg.src = data["network_capm"];
    networkCapmImg.style.width = "90%";
    capm.appendChild(networkCapmImg);

    showPortfolioValues(data, capm);

}

/**
 * Helper function to populate home page after user presses submit
 * @param {JSON object} data: JSON response after user submission for network 
 *  and CAPM info
 * @param {HTMLDivElement} capm: HTML div element representing contents for returns
 *  graph
 */
function showPortfolioValues(data, capm) {

    let ffEqualPortfolio = gen("h2");
    ffEqualPortfolio.textContent = "Fama & French Equal Portfolio";
    capm.appendChild(ffEqualPortfolio);

    ffEqualPortfolio = data['FF Equal Portfolio'];
    console.log(ffEqualPortfolio);
    for (let info in ffEqualPortfolio) {
        let infoElem = gen("p");
        infoElem.textContent = info + ": " + ffEqualPortfolio[info];
        capm.appendChild(infoElem);
    }
}

/**
 * Handle errors if they occur in a user-friendly manner
 * @param {Error} err 
 */
function handleError(err) {
    if (DEBUG) {
        console.log(err);
    } else {
        console.log(id('submit-result'));
        id("submit-result").textContent = 
        "We're having issues with our website. Please refresh or come back later!";
    }
}
init();
