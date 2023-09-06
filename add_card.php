import logging

logging.basicConfig(filename='/home/accessc/Documents/accessc.log', level=logging.INFO)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
pn532.SAM_configuration()
print("Waiting for NFC card...")
time.sleep(1)

while True:
    time.sleep(1.2)
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue
    else:
        print("Found card with UID:", [hex(i) for i in uid])
        newCard = [hex(i) for i in uid]

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M")

    mydb = mariadb.connect(
        host='localhost',
        user='accessc',
        password='abcd',
        database='codedb'
    )
    mycursor = mydb.cursor()

    print("Connected")
    print(newCard)
    print(today)

    mycursor.execute(f'SELECT EXISTS(SELECT * FROM accessc WHERE card = "{newCard}") as OUTPUT')
    myresult = mycursor.fetchone()[0]
    if myresult == 1:
        print("Card has already been issued")
        time.sleep(2)
        os.system("clear")
        return
    else:
        sql = f'INSERT INTO accessc (first, last, card, creation, access) VALUES ("{fname}", "{lname}", "{newCard}", "{today}", "{today}")'
        mycursor.execute(sql)
        time.sleep(2)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    logging.info(f'{fname, lname} and card have been written to database.')
    time.sleep(2)
    os.system('clear')



