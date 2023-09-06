function user_add() {
    echo "<br>";
    echo "<br>";
    $mydb = mariadb();
    $mycursor = $mydb->cursor();

    $fname = strtolower(readline("Enter First name: "));
    if ($fname == '') {
        echo "Name can not be blank";
        return;
    } else {
        echo $fname;
    }

    $lname = strtolower(readline("Enter last name: "));
    if ($lname == '') {
        echo "Name can not be blank";
        time_sleep(1);
    } else {
        echo $lname;
    }

    $query = "SELECT * FROM accessc WHERE first='{$fname}' AND last='{$lname}'";
    $mycursor->execute($query);
    $result = $mycursor->fetch();
    print_r($result);
    if (!$result) {
        echo "User's name is unique";
        logging_info("{$fname, $lname} was entered.");
        time_sleep(1);
    } else {
        echo "User already exists!";
        time_sleep(2);
        system('clear');
        user_add();
    }

    $spi = busio_SPI(board_SCK, board_MOSI, board_MISO);
    $cs_pin = DigitalInOut(board_D5);
    $pn532 = new PN532_SPI($spi, $cs_pin, false);
    $pn532->SAM_configuration();
    echo "Waiting for NFC card...";
    time_sleep(1);

    while (true) {
        time_sleep(1.2);
        $uid = $pn532->read_passive_target(timeout=0.5);
        if ($uid === NULL) {
            continue;
        } else {
            echo "Found card with UID: " . implode(" ", array_map('dechex', $uid));
            $newCard = array_map('dechex', $uid);
        }

        $now = new DateTime();
        $today = $now->format('d/m/Y H:i');

        $mydb = mariadb();    
        $mycursor = $mydb->cursor();

        if ($mydb->connect_error) {
            die("Connection failed: " . $mydb->connect_error);
        }

        echo "Connected";
        print_r($newCard);
        echo $today;

        $query = "SELECT EXISTS(SELECT * FROM accessc WHERE card = '{$newCard}') as OUTPUT";
        $mycursor->execute($query);
        $myresult = $mycursor->fetch()[0];
        if ($myresult == 1) {
            echo "Card has already been issued";
            time_sleep(2);
            system('clear');
            return; 
        } else {
            $sql = "INSERT INTO accessc (first, last, card, creation, access) VALUES ('{$fname}', '{$lname}', '{$newCard}', '{$today}', '{$today}')";
            $mycursor->execute($sql);
            time_sleep(2); 
        }
        $mydb->commit();
        echo $mycursor->rowcount . " record inserted.";
        logging_info("{$fname, $lname} and card have been written to database.");
        time_sleep(2);
        system('clear');
        return;
    }
}

