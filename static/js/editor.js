document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('textarea[name="content"]');
    const form = document.querySelector('form');
    const MAX_LENGTH = 200000; // 200k characters limit

    if (textarea) {
        // Auto-grow function
        function autoGrow(elem) {
            // Store current scroll position
            const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            elem.style.height = 'auto';
            elem.style.height = (elem.scrollHeight) + 'px';

            // Restore scroll position
            window.scrollTo(scrollLeft, scrollTop);
        }

        // Add input listener
        textarea.addEventListener('input', function() {
            autoGrow(textarea);
        });

        // Form submission validation
        if (form) {
            form.addEventListener('submit', function(e) {
                if (textarea.value.length > MAX_LENGTH) {
                    e.preventDefault();
                    alert(`Content is too long! Please reduce it to under ${MAX_LENGTH} characters. Current: ${textarea.value.length}`);
                }
            });
        }

        // Initialize on load
        autoGrow(textarea);
    }
}); 