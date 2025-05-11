# やきゅスコ バックエンドAPI

### ローカル起動コマンド

```
cd yakyusco_api
uvicorn main:app --reload
```

### Postgresコンテナ実行コマンド

```
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

### 参照記事

- <https://github.com/fastapi/sqlmodel/discussions/771>
- <https://github.com/fastapi/sqlmodel/discussions/735>
