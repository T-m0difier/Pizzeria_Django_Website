document.addEventListener('DOMContentLoaded', function () {
    const messages = JSON.parse(document.getElementById('django-messages').textContent);

    messages.forEach((message) => {
        Swal.fire({
            icon: message.tags.includes('success') ? 'success' :
                 message.tags.includes('info') ? 'info' :
                 message.tags.includes('warning') ? 'warning' :
                 message.tags.includes('error') ? 'error' : 'info',
            title: message.text,
            confirmButtonText: 'OK'
        });
    });
});

//This is my sweet alert messages functionality.
//It takes the messages that are already being displayed and makes them look better