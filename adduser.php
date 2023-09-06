<?php
// Database credentials
$servername = "localhost";
$username = "accessc";
$password = "abcd";
$dbname = "codedb";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "Connected successfully\n";

// Check if the user exists in the database
$fname = $_GET['fname'] ?? '';
$lname = $_GET['lname'] ?? '';

echo "First name: $fname<br>";
echo "Last name: $lname<br>";

$query = "SELECT * FROM accessc WHERE first='$fname' AND last='$lname'";
$result = $conn->query($query);

if ($result === false) {
    echo "Error executing query: " . $conn->error;
} else {
    if ($result->num_rows > 0) {
        echo "User already exists in the database.";
    } else {
        echo "User does not exist in the database.";

        // Execute Python script and display output
        $output = array();
        exec("python3 adduser.py $fname $lname", $output);
        echo "<div style='background-color:black; color:white; padding:10px;'>";
        foreach ($output as $line) {
            echo $line . '<br>';
        }
        echo "</div>";
    }
}

// Close the connection
$conn->close();
?>
