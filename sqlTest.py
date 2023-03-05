import mysql.connector

# Get user input for username, password, and hostname
username = input("Enter MySQL username (default is root): ") or "root"
password = input("Enter MySQL password: ")
hostname = input("Enter MySQL hostname (default is localhost): ") or "localhost"

try:
    # Try to connect to MySQL server
    conn = mysql.connector.connect(
        user=username,
        password=password,
        host=hostname
    )
    
    # If connection is successful, print success message
    print("Connection successful!")
    
    # Close the connection
    conn.close()
    
except mysql.connector.Error as err:
    # If connection fails, print error message
    print("Error message:", err)
