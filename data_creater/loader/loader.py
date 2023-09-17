import asyncio
import structs
import common
import aiohttp


async def load_points(point_ids: list):
    url = f"{common.Constants.server_base}/get_point_by_ids"
    async for batch in common.load_data_by_ids(
            url, point_ids, "point_ids", structs.Point):
        yield batch


async def load_measures(measure_ids: list):
    url = f"{common.Constants.server_base}/get_measures_by_ids"
    async for batch in common.load_data_by_ids(
        url, measure_ids, "measures_ids", structs.Measure):
        yield batch


async def load_data(data_ids: list):
    url = f"{common.Constants.server_base}/get_data_by_ids"
    async for batch in common.load_data_by_ids(
        url, data_ids, "data_ids", structs.Data, common.Constants.max_count_data):
        yield batch


async def load_train(train_ids: list):
    url = f"{common.Constants.server_base}/get_data_by_ids"
    async for batch in common.load_data_by_ids(
        url, train_ids, "train_ids", structs.Train):
        yield batch


async def get_points_by_trains(train_ids: list):
    headers = {"Content-Type": "application/json"}
    url = f"{common.Constants.server_base}/get_points_by_trains"
    for batch in common.create_batch(train_ids, common.Constants.max_count_trains_in_points_search):
        data={"train_ids": batch}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=data, headers=headers) as response:
                data = await response.json(content_type="application/json")
                yield {int(key): value for key, value in data.items()}


async def get_group_by_points(points_ids: list, max_diff_date=1440, min_size_group=3, need_group=False):
    headers = {"Content-Type": "application/json"}
    params = {
        "max_diff_date": str(max_diff_date),
        "min_size_group": str(min_size_group),
        "need_group": str(int(need_group))
    }
    url = f"{common.Constants.server_base}/get_grouped_data"
    for batch in common.create_batch(
            points_ids, common.Constants.max_count_points_in_group_search):
        data={"point_ids": batch}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, json=data, headers=headers, params=params) as response:
                data = await response.json(content_type="application/json")
                yield {
                    int(key): result 
                    for key, result in data.get("result", {}).items()
                }


async def main():
    common.init_constants("config.yaml")
    async for batch in get_group_by_points(list(range(30980, 35000))):
        print(batch)


if __name__ == "__main__":
    asyncio.run(main())
