import mysql.connector


# Connect to MySQL Database
def save_customer(name, address, salary, profile_photo):
    mydb = mysql.connector.connect(
        host="ijse-database.c1e684cqc92y.ap-south-1.rds.amazonaws.com",
        user="root",
        password="12345678",
    )

    mycursor = mydb.cursor()

    # Create the aws database if it doesn't exist
    mycursor.execute("SHOW DATABASES LIKE 'aws'")
    database_exists = mycursor.fetchone()
    if not database_exists:
        mycursor.execute("CREATE DATABASE aws")
        print("'aws' database created successfully!")

    # Use the 'aws' database
    mycursor.execute("USE aws")

    # Create the customer table only if it doesn't exist
    mycursor.execute("SHOW TABLES LIKE 'customer'")
    table_exists = mycursor.fetchone()
    if not table_exists:
        mycursor.execute("""
        CREATE TABLE customer (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            address VARCHAR(255),
            salary FLOAT,
            profile_photo VARCHAR(255)
        )
        """)
        print("'customer' table created successfully!")

    # Insert the record into the customer table
    mycursor.execute("""
    INSERT INTO customer (name, address, salary, profile_photo)
    VALUES (%s, %s, %s, %s)
    """, (name, address, salary, profile_photo))

    mydb.commit()
    print("Customer saved successfully!")

    mycursor.close()
    mydb.close()
