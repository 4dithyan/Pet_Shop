// ========================================
// DASHBOARD JAVASCRIPT
// Chart.js Initialization and Dashboard Logic
// ========================================

// Chart.js Global Configuration
Chart.defaults.font.family = "'Poppins', sans-serif";
Chart.defaults.color = '#64748B';

// Monthly Sales Chart
const monthlySalesCtx = document.getElementById('monthlySalesChart');
if (monthlySalesCtx) {
    const monthsData = JSON.parse(monthlySalesCtx.dataset.months || '[]');
    const revenuesData = JSON.parse(monthlySalesCtx.dataset.revenues || '[]');

    new Chart(monthlySalesCtx, {
        type: 'line',
        data: {
            labels: monthsData,
            datasets: [{
                label: 'Revenue (₹)',
                data: revenuesData,
                borderColor: '#2EC4B6',
                backgroundColor: 'rgba(46, 196, 182, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#2EC4B6',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: '#0F172A',
                    titleFont: {
                        size: 14,
                        weight: '700'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return 'Revenue: ₹' + context.parsed.y.toLocaleString('en-IN');
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: '#E2E8F0',
                        drawBorder: false
                    },
                    ticks: {
                        callback: function (value) {
                            return '₹' + value.toLocaleString('en-IN');
                        },
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}

// Order Status Distribution Chart
const orderStatusCtx = document.getElementById('orderStatusChart');
if (orderStatusCtx) {
    const statusLabels = JSON.parse(orderStatusCtx.dataset.labels || '[]');
    const statusCounts = JSON.parse(orderStatusCtx.dataset.counts || '[]');

    new Chart(orderStatusCtx, {
        type: 'doughnut',
        data: {
            labels: statusLabels,
            datasets: [{
                data: statusCounts,
                backgroundColor: [
                    '#2EC4B6',
                    '#FF6B6B',
                    '#FFD166',
                    '#10B981',
                    '#6366F1'
                ],
                borderWidth: 0,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 13,
                            weight: '600'
                        },
                        generateLabels: function (chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map((label, i) => {
                                    const value = data.datasets[0].data[i];
                                    return {
                                        text: `${label}: ${value}`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    backgroundColor: '#0F172A',
                    titleFont: {
                        size: 14,
                        weight: '700'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function (context) {
                            return context.label + ': ' + context.parsed + ' orders';
                        }
                    }
                }
            }
        }
    });
}

// Sidebar toggle for mobile
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.querySelector('.dashboard-sidebar');

if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 992) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        }
    });
}

// Animate stat counters on load
const statValues = document.querySelectorAll('.stat-value');
statValues.forEach(stat => {
    const targetValue = parseInt(stat.textContent.replace(/[^0-9]/g, ''));
    const isCurrency = stat.textContent.includes('₹');
    let currentValue = 0;
    const increment = targetValue / 50;
    const duration = 1500;
    const stepTime = duration / 50;

    const counter = setInterval(() => {
        currentValue += increment;
        if (currentValue >= targetValue) {
            clearInterval(counter);
            currentValue = targetValue;
        }

        if (isCurrency) {
            stat.textContent = '₹' + Math.floor(currentValue).toLocaleString('en-IN');
        } else {
            stat.textContent = Math.floor(currentValue).toLocaleString('en-IN');
        }
    }, stepTime);
});

// DataTable sorting and filtering
const initDataTable = (tableId) => {
    const table = document.getElementById(tableId);
    if (!table) return;

    const headers = table.querySelectorAll('th[data-sort]');
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', () => {
            sortTable(table, index);
        });
    });
};

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAscending = table.dataset.sortOrder === 'asc';

    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        if (!isNaN(aValue) && !isNaN(bValue)) {
            return isAscending ? aValue - bValue : bValue - aValue;
        } else {
            return isAscending ?
                aValue.localeCompare(bValue) :
                bValue.localeCompare(aValue);
        }
    });

    rows.forEach(row => tbody.appendChild(row));
    table.dataset.sortOrder = isAscending ? 'desc' : 'asc';
}

// Initialize tables
initDataTable('ordersTable');
initDataTable('productsTable');

// Real-time search
const searchInput = document.getElementById('dashboardSearch');
if (searchInput) {
    searchInput.addEventListener('input', debounce((e) => {
        const searchTerm = e.target.value.toLowerCase();
        const tableRows = document.querySelectorAll('.dashboard-table tbody tr');

        tableRows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    }, 300));
}

// Export to CSV
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => csvRow.push(col.textContent));
        csv.push(csvRow.join(','));
    });

    const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Attach export functionality to buttons
const exportButtons = document.querySelectorAll('[data-export]');
exportButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tableId = button.dataset.export;
        const filename = button.dataset.filename || 'export.csv';
        exportToCSV(tableId, filename);
    });
});

console.log('📊 Dashboard initialized with Chart.js!');
