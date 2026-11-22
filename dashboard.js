document.addEventListener('DOMContentLoaded', () => {
  const data = window.dashboardData || { history: [70, 75, 80, 85, 90], predictions: { Normal: 68, Warning: 22, Critical: 10 } };
  const performance = document.getElementById('performanceChart');
  if (performance && window.Chart) new Chart(performance, {
    type: 'line', data: { labels: ['Round 04', 'Round 05', 'Round 06', 'Round 07', 'Round 08'], datasets: [{ data: data.history, borderColor: '#5269e8', backgroundColor: 'rgba(82,105,232,.1)', borderWidth: 2.5, pointRadius: 4, pointHoverRadius: 6, pointBackgroundColor: '#fff', pointBorderColor: '#5269e8', pointBorderWidth: 2, tension: .38, fill: true }] },
    options: { maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { displayColors: false, callbacks: { label: ctx => ` ${ctx.parsed.y}% accuracy` } } }, scales: { x: { grid: { display: false }, border: { display: false }, ticks: { color: '#98a1b2', font: { family: 'DM Sans', size: 11 } } }, y: { min: 60, max: 100, ticks: { stepSize: 10, color: '#98a1b2', callback: v => `${v}%`, font: { family: 'DM Sans', size: 11 } }, grid: { color: '#edf0f5', drawTicks: false }, border: { display: false } } } }
  });
  const predictions = document.getElementById('predictionsChart');
  if (predictions && window.Chart) new Chart(predictions, { type: 'doughnut', data: { labels: ['Normal', 'Warning', 'Critical'], datasets: [{ data: [data.predictions.Normal, data.predictions.Warning, data.predictions.Critical], backgroundColor: ['#5369e8', '#f2ad4e', '#ed6d73'], borderWidth: 0, hoverOffset: 4 }] }, options: { cutout: '76%', maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed}%` } } } } });
  const picker = document.getElementById('file');
  const filename = document.getElementById('file-name');
  if (picker && filename) picker.addEventListener('change', () => { filename.textContent = picker.files.length ? `Selected: ${picker.files[0].name}` : ''; });
});
