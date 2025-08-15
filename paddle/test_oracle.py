import oracledb
from decouple import config

DB_USER = config("ORACLE_DB_USER")
DB_PASSWORD = config("ORACLE_DB_PASSWORD")
DB_HOST: str = str(config("ORACLE_DB_HOST", default=""))         # 'adb...oraclecloud.com' or 'localhost'
DB_PORT = config("ORACLE_DB_PORT", default=1522)    # 1522
DB_SERVICE : str = str(config("ORACLE_DB_SERVICE", default=""))
SSL_SERVER_DN : str = (config("ORACLE_SSL_SERVER_DN", default=""))

def build_dsn(host: str, port: int, service: str, ssl_dn: str) -> str:
    """
    Wallet-less TCPS DSN.
    - If host is localhost/127.0.0.1 (tunnel), DISABLE DN match (dev-only).
    - Else (direct to ADB), ENABLE DN match. You can optionally pin DN with ssl_server_cert_dn.
    """
    is_tunnel = host in ("localhost", "127.0.0.1")

    if is_tunnel:
        security = "(security=(ssl_server_dn_match=no))"
    else:
        # Strict hostname match; choose optional DN pin or comment it
        # security = f'(security=(ssl_server_dn_match=yes)(ssl_server_cert_dn="{ssl_dn}"))' if ssl_dn else "(security=(ssl_server_dn_match=yes))"
        security = "(security=(ssl_server_dn_match=yes))"

    dsn = (
        "(description="
          "(retry_count=20)"
          "(retry_delay=3)"
          f"(address=(protocol=tcps)(host={host})(port={port}))"
          f"(connect_data=(service_name={service}))"
          f"{security}"
        ")"
    )
    return dsn

dsn = build_dsn(DB_HOST, DB_PORT, DB_SERVICE, SSL_SERVER_DN)

print("🔍 Using DSN:", dsn)

try:
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn) as con:
        with con.cursor() as cur:
            cur.execute("select sysdate from dual")
            print("✅ Connection OK. SYSDATE:", cur.fetchone()[0])
except Exception as e:
    print("❌ Connection failed:", e)
