import os

def installdb():
    print("Initialize Database setting...")
    if os.path.exists(".dbinit"):
        print("Database initializing file found")
        return
    
    with open(".dbinit", "w") as f:
        f.write("""CREATE TABLE A (
    index INT,
    Name VARCHAR(255)
);

CREATE TABLE B (
    index INT,
    Name VARCHAR(255)
);

CREATE TABLE C (
    index INT,
    Name VARCHAR(255)
);

CREATE TABLE D (
    index INT,
    Name VARCHAR(255)
);
                """)
    
    print("Database Initialize Complete.")
    return