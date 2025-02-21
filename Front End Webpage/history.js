document.addEventListener("DOMContentLoaded", function () {
    fetch("http://127.0.0.1:5000/history")
        .then(response => response.json())
        .then(data => {
            let labels = data.map(entry => entry.date);
            let emissions = data.map(entry => entry.emission);

            let ctx = document.getElementById("historyChart").getContext("2d");

            new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Carbon Emissions Over Time",
                        data: emissions,
                        borderColor: "rgba(75, 192, 192, 1)",
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderWidth: 2
                    }]
                }
            });
        })
        .catch(error => console.error("Error fetching data:", error));
});
