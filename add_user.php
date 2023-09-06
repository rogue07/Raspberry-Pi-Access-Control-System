<?php
$mydb = new mysqli("localhost", "accessc", "abcd", "codedb");
if ($mydb->connect_error) {
    die("Connection failed: " . $mydb->connect_error);
}

$fname = $_POST['fname'];
$lname = $_POST['lname'];

$sql = "SELECT * FROM accessc WHERE first='$fname' AND last='$lname'";
$result = $mydb->query($sql);

if ($result->num_rows > 0) {
    echo "User already exists!<br>";
    // Redirect back to add_user_name.php
    header("Location: add_user_name.php?error=user-exists");
    exit;
} else {
    echo "User's name is unique<br>";
    error_log("$fname, $lname has been added to the database.");
}

$spi = new SPI();
$cs_pin = new DigitalInOut(5);
$pn532 = new PN532_SPI($spi, $cs_pin, false);
$pn532->SAM_configuration();

echo "Waiting for NFC card...<br>";
ob_flush();
flush();
sleep(1);

while (true) {
    $uid = $pn532->read_passive_target(0.5);

    if (!$uid) {
        continue;
    }

    echo "Found card with UID: " . implode(",", $uid) . "<br>";
    $newCard = implode(",", $uid);

    $now = date('d/m/Y H:i:s');

    $sql = "SELECT EXISTS(SELECT * FROM accessc WHERE card='$newCard') as OUTPUT";
    $result = $mydb->query($sql);
    $row = $result->fetch_assoc();

    if ($row["OUTPUT"] == 1) {
        echo "Card has already been issued<br>";
        ob_flush();
        flush();
        continue;
    }

    $sql = "INSERT INTO accessc (first, last, card, creation, access) VALUES ('$fname', '$lname', '$newCard', '$now', '$now')";
    $mydb->query($sql);

    if ($mydb->affected_rows > 0) {
        echo $mydb->affected_rows . " record inserted.<br>";
        error_log("$fname, $lname and card have been written to database.");
        ob_flush();
        flush();
        break;
    } else {
        echo "Error inserting record.<br>";
        ob_flush();
        flush();
        return;
    }
}
?>
