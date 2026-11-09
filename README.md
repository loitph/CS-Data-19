

### Local setup:
```
1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
```


docker run --platform linux/amd64 \
  --name loitph-mssql-2026 --hostname loitph-mssql-2026 \
  -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=MySQL#2026" \
  -p 1433:1433 \
  -v loitph-mssql-2026-data:/var/opt/mssql \
  mcr.microsoft.com/mssql/server:2025-latest

docker start -a loitph-mssql-2026