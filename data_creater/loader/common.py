import aiohttp
import yaml


class Constants:
    # Заполнить вручную у себя 
    server_base = ""
    # Не увеличивать лимиты, работать не будет
    # Это лимиты
    max_count_points = 100
    max_count_trains = 100
    max_count_measures = 100
    max_count_data = 80
    # максимальное число Train-ов которые можно запросить
    # для получения Point по ним
    max_count_trains_in_points_search = 100
    max_count_points_in_group_search = 100


def init_constants(config_path: str):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        for key, value in config.items():
            if key == "server_base":
                Constants.server_base = value
            if key == "max_count_points":
                Constants.max_count_points = value
            if key == "max_count_trains":
                Constants.max_count_trains = value
            if key == "max_count_measures":
                Constants.max_count_measures = value
            if key == "max_count_data":
                Constants.max_count_data = value
            if key == "max_count_trains_in_points_search":
                Constants.max_count_trains_in_points_search = value
            if key == "max_count_points_in_group_search":
                Constants.max_count_points_in_group_search = value


def create_batch(data: list, max_batch: int):
    for begin in range(0, len(data), max_batch):
        end = min(len(data), begin + max_batch)
        yield data[begin: end]


async def load_data_by_ids(url: str, ids: list, ids_keyword: str, data_type, batch_size: int = 100):
    for batch in create_batch(ids, batch_size):
        loaded_data = []
        data={ids_keyword: batch}
        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=data, headers=headers) as response:
                data = await response.json(content_type="application/json")
                if "error" in data:
                    continue
                results = data.get("result", {})
                for values in results.values():
                    if not values:
                        continue
                    loaded_data.append(data_type(**values))
                yield loaded_data
