document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll('input');
    let tooltipTimeout;

    function showTooltip(input) {
        const tooltipId = 'tooltip' + input.id.charAt(0).toUpperCase() + input.id.slice(1);
        const tooltip = document.getElementById(tooltipId);

        if (tooltip) {
            const inputRect = input.getBoundingClientRect();
            const tooltipHeight = tooltip.getBoundingClientRect().height;

            tooltip.style.top = inputRect.top + inputRect.height + 5 + 'px';
            tooltip.style.left = inputRect.left + 'px';

            tooltip.classList.add('visible');
        }
    }

    function hideTooltip(input) {
        const tooltipId = 'tooltip' + input.id.charAt(0).toUpperCase() + input.id.slice(1);
        const tooltip = document.getElementById(tooltipId);
        if (tooltip) {
            tooltip.classList.remove('visible');
        }
    }

    inputs.forEach(input => {
        input.addEventListener('mouseenter', function () {
            // Mostrar el tooltip después de 2 segundos
            tooltipTimeout = setTimeout(function() {
                showTooltip(input);
            }, 1000);
        });

        input.addEventListener('mouseleave', function () {
            // Cancelar el retraso si el mouse sale antes de 2 segundos
            clearTimeout(tooltipTimeout);
            hideTooltip(input);
        });
    });
});