import psycopg2

HOSTS = [
    "pgm-bp12c046yz7tejie5o.pg.rds.aliyuncs.com",
    "pgm-bp12c046yz7tejie.pg.rds.aliyuncs.com",
]
USER = "xtwq666"
PASSWORD = "Lzhmima123!"
DB = "tutusys"

for host in HOSTS:
    try:
        conn = psycopg2.connect(
            host=host, port=5432, database=DB, user=USER, password=PASSWORD, connect_timeout=8
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM information_schema.tables "
            "WHERE table_schema='public' AND table_type='BASE TABLE'"
        )
        tables = cur.fetchone()[0]
        bunnies = "-"
        if tables:
            cur.execute("SELECT COUNT(*) FROM bunnies")
            bunnies = cur.fetchone()[0]
        print(f"{host} -> tables={tables}, bunnies={bunnies}")
        conn.close()
    except Exception as e:
        print(f"{host} -> ERROR: {e}")
