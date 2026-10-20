# githubwork

个人项目仓库，按日期版本（`vYYYY.MM.DD`）持续更新。

## 项目

| 项目 | 说明 | 入口 |
|---|---|---|
| [whereToGo](./whereToGo/) | 石家庄周边游 · 筛选 & 随机转盘（131 个景点，纯前端单页） | [index.html](./whereToGo/index.html) |

## 版本

- 每天更新后以 `vYYYY.MM.DD` 标签标记一个版本，可在仓库的 **Tags** 中查看。

## 维护说明

- `whereToGo` 的景点数据以 `attractions.json` 为**唯一数据源**；修改后运行 `python build.py` 重新生成页面内嵌数据与 CSV。
