# reference/maps.md — 出图（把老地名套到现代地图上）

用途：当用户想看"这些老地名**今天落在哪一片**"，生成一张**离线图**。

## 一句话命令

```
py code/city_map.py 香港 --open
```

→ 生成 `artifacts/香港_overlay.svg`，用浏览器打开（**不联网**）。

## 原理

1. `code/basemaps.json` 里配了每个城市的**现代底图**及其**经纬度范围**。
2. `code/city_map.py` 调 `code/overlay_on_image.py`：把该城有坐标的地名
   （`place.lat/lon`）按"经纬度 → 像素"映射到底图上，画成红点＋名字，输出 SVG
   （底图**内联**进去，所以离线也能看）。

## 目前配置

- **香港**：底图 = 维基百科 `China Hong Kong location map.svg`
  （作者 Maximilian Dörrbecker / Chumwa，**CC BY-SA 3.0**；
  范围 22.12–22.57°N / 113.82–114.45°E）。
- 其余城市：未配（要加城时，找一张维基"位置图"或你提供的现代地图，
  把它的 `image` 与 `min/max` 经纬度填进 `basemaps.json` 即可）。

## 注意

- 坐标是**对照、近似**（source 7），只作方位示意。
- 底图有版权（CC BY-SA 等）：图角会带**署名**；对外分享时须保留。
- 图里只画**有坐标**的地名；没坐标的点不会出现。
