def save_file(data: str, url: str) -> None:
    """Записывает в файл"""
    short_uri = url.split("/")[-1]
    with open(f"app/data/{short_uri}.txt","w",encoding="utf-8") as f:
        f.write(data)
