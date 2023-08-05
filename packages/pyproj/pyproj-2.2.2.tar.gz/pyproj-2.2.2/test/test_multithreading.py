import concurrent.futures

from pyproj import Transformer

TRANSFORMER = Transformer.from_crs(4326, 3857)


def transform_point(aa):
    print(f"{aa}: {TRANSFORMER.transform((12, 11), (13, 12))}")


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(transform_point, range(20))
