import os

def install():
    if os.path.exists(".env"):
        print(".env 파일이 이미 존재합니다.")
        return
    
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
    
    print("env install complete.")
    return
