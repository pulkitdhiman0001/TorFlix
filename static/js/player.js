document.addEventListener('DOMContentLoaded', () => {
        const player = new Plyr('video', {
            // Configuration options can be added here
        });
    });



document.addEventListener('DOMContentLoaded', () => {
        const player = new Plyr('video', {
            controls: ['play', 'progress', 'current-time', 'mute', 'volume', 'fullscreen'],
            settings: [],
            autoplay: false,
            loop: false,
            // Add more options as needed
        });
    });


// Initialize Plyr on the audio element
const player = new Plyr('audio');