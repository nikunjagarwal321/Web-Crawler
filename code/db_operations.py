from sqlite3 import Error, connect

db_path = "example.db"

# create database
def create_database():
    try:
        create_table("crawled_links", ["link", "parent_link"], ["text", "text"])
        create_table("queued_links", ["link", "parent_link"], ["text", "text"])
        create_table("foreign_links", ["link", "parent_link", "type"], ["text", "text", "text CHECK( type in ('all-amazon','non-amazon'))"])
        create_table("error_links", ["link", "parent_link", "response", "type"], ["text", "text", "text", "text CHECK( type in ('dev-amazon','all-amazon','non-amazon'))"])
    except Error as e:
        print(e)

# connect to database
def get_db():
    con = connect(db_path)
    cur = con.cursor()
    return con, cur

# close database
def close_db(con):
    con.commit()
    con.close()

# create tables
def create_table(table_name, column_names, column_types):
    try :
        con, cur = get_db()
        command = "CREATE TABLE {tn} ({cn} {ct} CONSTRAINT pk PRIMARY KEY)"\
            .format(tn=table_name, cn=column_names[0], ct=column_types[0])
        cur.execute(command)
        i = 1
        while i < len(column_names):
            cur.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
            .format(tn=table_name, cn=column_names[i], ct=column_types[i]))
            i = i + 1
        close_db(con)
    except Error as e:
        print(e)

# insert links into table
def insert_links_to_db(table_name, links):
    if len(links) < 1:
        return
    con, cur = get_db()
    no_of_columns = len(list(links)[0]) 
    if no_of_columns == 2:
        command = "INSERT into {tn} VALUES (?,?)".format(tn=table_name)
    elif no_of_columns == 3:
        command = "INSERT into {tn} VALUES (?,?,?)".format(tn=table_name)
    elif no_of_columns == 4:
        command = "INSERT into {tn} VALUES (?,?,?,?)".format(tn=table_name)
    for link in links:
        try:
            cur.execute(command, link)
        except Error:
            pass
    close_db(con)
    
    

# retrieve data from database
def retrieve_links_from_db(table_name):
    con, cur = get_db()
    command = "SELECT * from {tn} ".format(tn=table_name)
    cur.execute(command)
    links = cur.fetchall()
    cur.execute(command)
    close_db(con)
    return set(links)
