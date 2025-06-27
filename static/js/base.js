// Base JS – future logic or chart initializations here

document.addEventListener('DOMContentLoaded', function () {
  const chartElement = document.getElementById('salesChart');
  if (chartElement) {
    const ctx = chartElement.getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
          label: 'Sales ($)',
          data: [5000, 7000, 4000, 8000, 6000],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }
});
