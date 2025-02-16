import mysql.connector


# Connect to MySQL Database
def save_customer_to_db(name, address, salary, profile_photo):
    mydb = mysql.connector.connect(
        host="ijse-database.c1e684cqc92y.ap-south-1.rds.amazonaws.com",
        user="root",
        password="12345678",
    )

    mycursor = mydb.cursor()
    mycursor.execute("USE aws")

    # Create the customer table if it doesn't exist
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255),
        salary FLOAT,
        profile_photo VARCHAR(255)
    )
    """)
    mydb.commit()

    # Insert the record into the customer table
    mycursor.execute("""
    INSERT INTO customer (name, address, salary, profile_photo)
    VALUES (%s, %s, %s, %s)
    """, (name, address, salary, profile_photo))

    mydb.commit()

    print("Customer Saved Successfully...!")
