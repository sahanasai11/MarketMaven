"use strict";

const ROOTPATH = "http://localhost:5000";
const DEBUG = true;

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
            id("submit-result").textContent = "Successfully submitted!";
        } catch (err) {
            handleError(err);
        } 
    }); 
}

function populateIndex(data) {
    console.log(data);

    let networkCard = id("network-card");
    let capmCard = id("returns-card");

    let networkImg = gen("img");
    networkImg.src = data["network_img"];
    networkImg.style.width = "90%";
    networkCard.appendChild(networkImg);

    let networkCapmImg = gen("img");
    networkCapmImg.src = data["network_capm"];
    networkCapmImg.style.width = "90%";
    capmCard.appendChild(networkCapmImg);
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
