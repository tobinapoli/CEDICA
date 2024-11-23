function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.flashes .alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show'); 
            alert.classList.add('fade'); o
            setTimeout(() => alert.remove(), 300); 
        }, 4000); 
    });
}

document.addEventListener('DOMContentLoaded', autoDismissAlerts);