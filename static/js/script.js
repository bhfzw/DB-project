// Базовые функции JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое скрытие alert через 5 секунд
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите выполнить это действие?')) {
                e.preventDefault();
            }
        });
    });
});
