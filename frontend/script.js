let energyChart = null;

document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const payload = {
        T1: parseFloat(document.getElementById('T1').value),
        RH_1: 47.0,
        T2: 20.0, RH_2: 44.0,
        T3: 22.0, RH_3: 40.0,
        T_out: parseFloat(document.getElementById('T_out').value),
        RH_out: 92.0,
        hour: parseInt(document.getElementById('hour').value),
        day: 15, weekday: 2,
        energy_previous: parseFloat(document.getElementById('energy_previous').value),
        energy_1_step_ago: parseFloat(document.getElementById('energy_1_step_ago').value),
        energy_2_step_ago: parseFloat(document.getElementById('energy_2_step_ago').value)
    };

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Sonuçları göster
        document.getElementById('results').style.display = 'block';
        document.getElementById('res-wh').innerText = data.prediction_wh;
        document.getElementById('res-cost').innerText = data.cost_tl;
        document.getElementById('res-co2').innerText = data.co2_kg;

        // Grafiği Güncelle
        updateChart(data.prediction_wh);

    } catch (err) {
        alert("Tahmin alınırken hata oluştu: " + err);
    }
});

function updateChart(predictedValue) {
    const ctx = document.getElementById('energyChart').getContext('2d');
    
    if (energyChart) { energyChart.destroy(); }

    energyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['2 Saat Önce', '1 Saat Önce', 'Anlık Tüketim', 'Tahmin Edilen (Gelecek)'],
            datasets: [{
                label: 'Enerji Tüketimi (Wh)',
                data: [
                    parseFloat(document.getElementById('energy_2_step_ago').value),
                    parseFloat(document.getElementById('energy_1_step_ago').value),
                    parseFloat(document.getElementById('energy_previous').value),
                    predictedValue
                ],
                backgroundColor: ['#64748b', '#64748b', '#0284c7', '#4ade80']
            }]
        },
        options: { responsive: true, plugins: { legend: { display: false } } }
    });
}
