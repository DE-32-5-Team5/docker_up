import os

def install():
    if os.path.exists(".env"):
        print("env setting file found")
        return
    
    else:
        print("Initialize env setting...")
        root_password = input("Enter Database root password : ")
        database = input("Enter Database Name : ")
        user_name = input("Enter User Name : ")
        user_password = input("Enter user Password : ")
    
        with open(".env", "w") as f:
            f.write(f"MARIADB_ROOT_PASSWORD={root_password}\n")
            f.write(f"MARIADB_DATABASE={database}\n")
            f.write(f"MARIADB_USER={user_name}\n")
            f.write(f"MARIADB_PASSWORD={user_password}\n")
    
    if os.path.exists("docker/db/config/.my.cnf"):
        print("cnf setting file found")
        return
    
    else:
        with open("docker/db/.my.cnf", "w") as f:
            f.write(f"user={user_name}\n")
            f.write(f"password={user_password}\n")
            f.write(f"host=localhost\n")
            f.write(f"port=3551\n")

    print("env, exporter cnf install complete.")
    return
