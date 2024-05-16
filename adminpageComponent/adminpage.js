function logout() {
    // Perform logout actions here, such as clearing session data
    // Redirect the user to the login page
    window.location.href = 'adminlogin.html';
}

// Prevent navigating back to admin page after logout
window.addEventListener('popstate', function(event) {
    window.history.pushState(null, document.title, window.location.href);
});


// total_files = 0

function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    if (!file) {
        alert('Please select a file.');
        return;
    }
    if(file.name.slice(-4) != '.pdf'){
        alert('Please select a pdf file.')
        return;
    }
    var formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:8000/fileupload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert('File uploaded successfully!');
            // x = total_files += 1
            // alert(x + ' files uploaded successfully')
        } else {
            alert('Error uploading file.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading file.');
    });
}

function createdb() {
    var overlay = document.getElementById('overlay');
    var overlayMessage = document.getElementById('overlay-message');
    overlay.style.display = 'block'; // Show the overlay
    overlayMessage.innerText = 'Please wait, creating database...'; // Show loading message

    fetch('http://localhost:8000/createdb', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            alert('Database created successfully!');
            return response.json();
        } else {
            alert('Error creating database.');
        }
    })
    .then(data => {
        console.log('Response:', data);
        console.log(data.message);
        alert('Database created successfully!');
        overlay.style.display = 'none'; // Hide the overlay when response received
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating database.');
        overlay.style.display = 'none'; // Hide the overlay on error too
    });
}

// function showdb() {
//     var overlay = document.getElementById('overlay');
//     var overlayMessage = document.getElementById('overlay-message');
//     overlay.style.display = 'block'; // Show the overlay
//     overlayMessage.innerText = 'Please wait, fetching data from database...'; // Show loading message

//     fetch('http://localhost:8000/showdb', {
//         method: 'GET'
//     })
//     .then(response => {
//         if (response.ok) {
//             return response.json();
//         } else {
//             throw new Error('Error fetching data from database.');
//         }
//     })
//     .then(data => {
//         // Display the data on the screen, for example, in an alert
//         alert(JSON.stringify(data));
//         overlay.style.display = 'none'; // Hide the overlay when response received
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('Error fetching data from database.');
//         overlay.style.display = 'none'; // Hide the overlay on error too
//     });
// }

function showdb() {
    var overlay = document.getElementById('overlay');
    var overlayMessage = document.getElementById('overlay-message');
    overlay.style.display = 'block'; // Show the overlay
    overlayMessage.innerText = 'Please wait, fetching data from database...'; // Show loading message

    fetch('http://localhost:8000/showdb', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            return response.text(); // Note: Using response.text() instead of response.json()
        } else {
            throw new Error('Error fetching data from database.');
        }
    })
    .then(data => {
        
        var dataDisplay = document.getElementById('dataDisplay');
        dataDisplay.innerHTML = '<h3>Data from Database:</h3>';
        dataDisplay.innerHTML += '<p>' + data  + '</p>';

        overlay.style.display = 'none'; // Hide the overlay when response received
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error fetching data from database.');
        overlay.style.display = 'none'; // Hide the overlay on error too
    });
}
