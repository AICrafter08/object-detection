function displayTrackIds(trackids) {
    const container = d3.select('#dictionary-data');
    container.html(''); // Clear previous content
    Object.entries(trackids).forEach(([key, value]) => {
        container.append('p').text(`${key}: ${value.join(', ')}`);
    });
}

function renderUniqueCountBarChart(unique_count) {
    const data = Object.entries(unique_count).map(([key, value]) => ({ name: key, value }));

    const totalSum = data.reduce((accumulator, currentValue) => accumulator + currentValue.value, 0);

    console.log("Total sum of values:", totalSum);
    const svgWidth = 400, svgHeight = 300, barPadding = 10;
    const barWidth = (svgWidth / data.length);

    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

    const svg = d3.select('#data-visualization')
        .append('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight);

    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('y', (d) => svgHeight - (d.value * 300/totalSum))
        .attr('height', (d) => (d.value * 300/totalSum))
        .attr('width', barWidth - barPadding)
        .attr('transform', (d, i) => {
            const translate = [barWidth * i, 0];
            return `translate(${translate})`;
        })
        .style('fill', (d, i) => colorScale(i));;

    svg.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .text((d) => `${d.name} (${d.value})`)
        .attr('y', (d) => svgHeight - (d.value * 300/totalSum) - 10)
        .attr('x', (d, i) => barWidth * i + (barWidth / 2) - barPadding)
        .attr('text-anchor', 'middle');
}

async function uploadProcessedVideo(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch('http://127.0.0.1:8000/upload_video/', {
        method: 'POST',
        body: formData
    });
    return response.json();
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        // First upload the video
        uploadProcessedVideo(file).then(data => {
            sessionStorage.clear();
            // Here you would save the path returned from the server
            sessionStorage.setItem('videoPath', data.path);
            // Assuming the file upload endpoint returns the path in the response
        }).catch(error => console.error('Error:', error));

        // Now display the video locally
        const uploadedVideo = document.getElementById('uploadedVideo');
        uploadedVideo.src = URL.createObjectURL(file);
        uploadedVideo.load();
        uploadedVideo.addEventListener('loadedmetadata', function () {
            const videoContainer = document.getElementById('video-container');
            const ratio = (this.videoHeight / this.videoWidth) * 100;
            videoContainer.style.paddingTop = ratio + '%';
        });
    }
}

function saveAndProcess() {
    const videoPath = sessionStorage.getItem('videoPath');
    if (videoPath) {
        document.getElementById('spinner-overlay').style.display = 'flex';
        const data = {
            video_path: { path: videoPath },
            output_path: { path: 'videos/output_file.webm' } // Ensure this is a valid server path where the output should be saved
        };

        fetch('http://127.0.0.1:8000/count_objects/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                alert(data.output_file); // Popup message from the server
                document.getElementById('spinner-overlay').style.display = 'none';
                // Save the path of the processed video returned from the server
                sessionStorage.setItem('processedVideoPath', data.output_file);
                sessionStorage.setItem('processedtrackids', JSON.stringify(data.trackids));
                sessionStorage.setItem('processedunique_count', JSON.stringify(data.unique_count));
                displayProcessedVideo(data.output_file); // Update the source of the video element
                displayTrackIds(data.trackids);
                renderUniqueCountBarChart(data.unique_count);
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('spinner-overlay').style.display = 'none';
            });
    } else {
        alert("Please upload video again.");
    }
}

// Define displayUploadedVideo similar to displayProcessedVideo
function displayUploadedVideo(uploadedVideoPath) {
    const uploadedVideo = document.getElementById('uploadedVideo');
    if (uploadedVideo) {
        uploadedVideo.src = uploadedVideoPath; // Assuming the path is directly usable as a URL
        uploadedVideo.load(); // Load and display the video
        uploadedVideo.addEventListener('loadedmetadata', function () {
            const videoContainer = document.getElementById('video-container');
            const ratio = (this.videoHeight / this.videoWidth) * 100;
            videoContainer.style.paddingTop = ratio + '%'; // Adjust container padding to maintain aspect ratio
        });
    } else {
        console.error('Uploaded video element not found');
    }
}

function displayProcessedVideo(processedVideoPath) {
    const processedVideo = document.getElementById('processedVideo');
    if (processedVideo) {
        console.log(processedVideoPath)
        // Set the source to the processed video path
        processedVideo.src = processedVideoPath;
        processedVideo.load(); // Load and display the video
        processedVideo.addEventListener('loadedmetadata', function () {
            const videoContainer = document.getElementById('processed-video-container');
            const ratio = (this.videoHeight / this.videoWidth) * 100;
            videoContainer.style.paddingTop = ratio + '%'; // Adjust container padding to maintain aspect ratio
        });
    } else {
        console.error('Processed video element not found');
    }
}


function init() {
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.addEventListener('change', handleFileUpload);

    // Immediately attempt to display uploaded and processed videos if their paths are in session storage
    const uploadedVideoPath = sessionStorage.getItem('videoPath');
    const processedVideoPath = sessionStorage.getItem('processedVideoPath');
    const processedtrackids = JSON.parse(sessionStorage.getItem('processedtrackids'));
    const processedunique_count = JSON.parse(sessionStorage.getItem('processedunique_count'));


    if (uploadedVideoPath) {
        // Assuming the server transforms the path into a URL or a path accessible by the client
        displayUploadedVideo(uploadedVideoPath); // You need to define this function
    }

    if (processedVideoPath) {
        displayProcessedVideo(processedVideoPath);
    }

    if (processedtrackids) {
        displayTrackIds(processedtrackids);
    }

    if (processedunique_count) {
        renderUniqueCountBarChart(processedunique_count);
    }       
}

window.onload = init;