// placeholder_script.js

document.addEventListener("DOMContentLoaded", function () {
    // Set placeholder for TeamA
    var teamASelect = document.getElementById("id_TeamA");
    var placeholderOptionA = document.createElement("option");
    placeholderOptionA.text = "Select Team A";
    placeholderOptionA.value = "";
    teamASelect.add(placeholderOptionA, teamASelect.options[0]);

    // Set placeholder for TeamB
    var teamBSelect = document.getElementById("id_TeamB");
    var placeholderOptionB = document.createElement("option");
    placeholderOptionB.text = "Select Team B";
    placeholderOptionB.value = "";
    teamBSelect.add(placeholderOptionB, teamBSelect.options[0]);
});
