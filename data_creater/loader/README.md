# Установка зависимостей
Создать и подключиться к venv
```
python3 -m venv venv
source venv/bin/activate
```
Из корня проекта запустить:
```
pip install -r requirements.txt
```


# Пример

Для того чтобы все заработало, заполните в файле structs.py 
```
import loader
import common


# async перед def нужно писать, иначе не запустится
async def main():
    # Тут нужно указать путь к конфигу
    common.init_constants("config.yaml")

    # Айдишники Point которые вернет сервер
    point_ids = list(range(30980, 35000))

    # Данные выгружаются батчами, чтобы не гонять большие массивы данных
    # за один раз
    async for batch in loader.get_group_by_points(point_ids):
        print(batch)


if __name__ == "__main__":
    # asyncio.run нужно писать иначе не заработает
    asyncio.run(main())
```
