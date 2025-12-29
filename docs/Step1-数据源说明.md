# Step1 - 数据源说明文档

## 1. 数据集概述

### 1.1 数据集来源

**TMDB 5000 Movie Dataset**

- **来源平台**: Kaggle
- **数据集链接**: [https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- **原始数据源**: [The Movie Database (TMDB)](https://www.themoviedb.org/)
- **数据收集时间**: 2017年
- **许可证**: CC0: Public Domain

### 1.2 数据集描述

该数据集包含约5000部电影的元数据信息，涵盖电影基本信息、票房数据、评分数据以及演职人员信息。数据来源于TMDB（The Movie Database），是一个由社区维护的电影数据库。

### 1.3 文件组成

| 文件名 | 记录数 | 描述 |
|--------|--------|------|
| `tmdb_5000_movies.csv` | 4803 | 电影基本信息、票房、评分等 |
| `tmdb_5000_credits.csv` | 4803 | 电影演职人员信息 |

---

## 2. 字段说明

### 2.1 tmdb_5000_movies.csv

该文件包含20个字段，详细描述如下：

| # | 字段名 | 数据类型 | 描述 | 示例值 |
|---|--------|----------|------|--------|
| 1 | `budget` | Integer | 电影预算（美元） | 237000000 |
| 2 | `genres` | JSON Array | 电影类型列表 | `[{"id": 28, "name": "Action"}]` |
| 3 | `homepage` | String | 电影官方网站URL | `http://www.avatarmovie.com/` |
| 4 | `id` | Integer | TMDB电影唯一标识符 | 19995 |
| 5 | `keywords` | JSON Array | 电影关键词标签 | `[{"id": 1463, "name": "culture clash"}]` |
| 6 | `original_language` | String | 电影原始语言（ISO 639-1） | `en`, `zh`, `ja` |
| 7 | `original_title` | String | 电影原始标题 | Avatar |
| 8 | `overview` | String | 电影剧情简介 | In the 22nd century... |
| 9 | `popularity` | Float | TMDB热度评分 | 150.437577 |
| 10 | `production_companies` | JSON Array | 制作公司列表 | `[{"name": "Pixar", "id": 3}]` |
| 11 | `production_countries` | JSON Array | 制作国家列表 | `[{"iso_3166_1": "US", "name": "United States"}]` |
| 12 | `release_date` | Date | 上映日期（YYYY-MM-DD） | 2009-12-10 |
| 13 | `revenue` | Integer | 票房收入（美元） | 2787965087 |
| 14 | `runtime` | Float | 电影时长（分钟） | 162.0 |
| 15 | `spoken_languages` | JSON Array | 电影语言列表 | `[{"iso_639_1": "en", "name": "English"}]` |
| 16 | `status` | String | 发行状态 | Released, Post Production |
| 17 | `tagline` | String | 电影宣传语 | Enter the World of Pandora. |
| 18 | `title` | String | 电影标题 | Avatar |
| 19 | `vote_average` | Float | 平均评分（0-10） | 7.2 |
| 20 | `vote_count` | Integer | 投票人数 | 11800 |

#### 2.1.1 JSON字段结构详解

**genres（电影类型）**
```json
[
  {"id": 28, "name": "Action"},
  {"id": 12, "name": "Adventure"},
  {"id": 14, "name": "Fantasy"}
]
```

**keywords（关键词）**
```json
[
  {"id": 1463, "name": "culture clash"},
  {"id": 2964, "name": "future"},
  {"id": 3386, "name": "space war"}
]
```

**production_companies（制作公司）**
```json
[
  {"name": "Ingenious Film Partners", "id": 289},
  {"name": "Twentieth Century Fox Film Corporation", "id": 306}
]
```

**production_countries（制作国家）**
```json
[
  {"iso_3166_1": "US", "name": "United States of America"},
  {"iso_3166_1": "GB", "name": "United Kingdom"}
]
```

**spoken_languages（语言）**
```json
[
  {"iso_639_1": "en", "name": "English"},
  {"iso_639_1": "es", "name": "Español"}
]
```

---

### 2.2 tmdb_5000_credits.csv

该文件包含4个字段，详细描述如下：

| # | 字段名 | 数据类型 | 描述 | 示例值 |
|---|--------|----------|------|--------|
| 1 | `movie_id` | Integer | 电影ID（与movies.csv的id关联） | 19995 |
| 2 | `title` | String | 电影标题 | Avatar |
| 3 | `cast` | JSON Array | 演员列表 | 见下方结构 |
| 4 | `crew` | JSON Array | 剧组人员列表 | 见下方结构 |

#### 2.2.1 cast（演员）字段结构

```json
{
  "cast_id": 242,
  "character": "Jake Sully",
  "credit_id": "5602a8a7c3a3685532001c9a",
  "gender": 2,
  "id": 65731,
  "name": "Sam Worthington",
  "order": 0
}
```

| 子字段 | 类型 | 描述 |
|--------|------|------|
| `cast_id` | Integer | 演员在该电影中的唯一ID |
| `character` | String | 饰演的角色名称 |
| `credit_id` | String | 演职记录唯一标识 |
| `gender` | Integer | 性别（0: 未知, 1: 女, 2: 男） |
| `id` | Integer | 演员的TMDB人员ID |
| `name` | String | 演员姓名 |
| `order` | Integer | 演员排序（0为主演） |

#### 2.2.2 crew（剧组人员）字段结构

```json
{
  "credit_id": "52fe48009251416c750aca23",
  "department": "Directing",
  "gender": 2,
  "id": 2710,
  "job": "Director",
  "name": "James Cameron"
}
```

| 子字段 | 类型 | 描述 |
|--------|------|------|
| `credit_id` | String | 演职记录唯一标识 |
| `department` | String | 所属部门 |
| `gender` | Integer | 性别（0: 未知, 1: 女, 2: 男） |
| `id` | Integer | 人员的TMDB人员ID |
| `job` | String | 职位名称 |
| `name` | String | 人员姓名 |

**常见department值**:
- Directing（导演部门）
- Writing（编剧部门）
- Production（制片部门）
- Camera（摄影部门）
- Editing（剪辑部门）
- Art（美术部门）
- Sound（音效部门）
- Costume & Make-Up（服装化妆部门）

**常见job值**:
- Director（导演）
- Producer（制片人）
- Executive Producer（执行制片人）
- Screenplay（编剧）
- Director of Photography（摄影指导）
- Original Music Composer（原创音乐作曲）
- Editor（剪辑师）

---

## 3. 数据关联

两个数据文件通过以下字段关联：

```
tmdb_5000_movies.csv.id  <-->  tmdb_5000_credits.csv.movie_id
```

关联示例：
```sql
SELECT m.*, c.cast, c.crew
FROM movies m
JOIN credits c ON m.id = c.movie_id
```

---

## 4. 数据质量说明

### 4.1 数据完整性

| 字段 | 缺失情况 | 说明 |
|------|----------|------|
| `budget` | 部分为0 | 部分电影预算未公开 |
| `revenue` | 部分为0 | 部分电影票房未公开 |
| `homepage` | 约50%缺失 | 老电影通常无官网 |
| `tagline` | 约20%缺失 | 部分电影无宣传语 |
| `overview` | 极少缺失 | 几乎所有电影都有简介 |
| `runtime` | 少量缺失 | 个别电影时长未知 |

### 4.2 数据清洗建议

1. **预算和票房为0的处理**
   - 筛选 `budget > 0` 和 `revenue > 0` 进行ROI分析
   - 或使用中位数/均值填充

2. **JSON字段解析**
   - 使用 `ast.literal_eval()` 或 `json.loads()` 解析
   - 提取嵌套字段中的 `name` 值

3. **日期处理**
   - 将 `release_date` 转换为 datetime 类型
   - 提取年份用于时间序列分析

4. **异常值处理**
   - 检查预算和票房的异常高/低值
   - 验证评分范围（0-10）

---

## 5. 数据统计概览

### 5.1 基础统计

| 指标 | 值 |
|------|-----|
| 电影总数 | 4803 |
| 时间范围 | 1916 - 2017 |
| 平均预算 | ~$29M |
| 平均票房 | ~$82M |
| 平均评分 | 6.09 |
| 平均时长 | 106分钟 |

### 5.2 电影类型分布（Top 10）

| 类型 | 数量 |
|------|------|
| Drama | 2297 |
| Comedy | 1722 |
| Thriller | 1274 |
| Action | 1154 |
| Romance | 885 |
| Adventure | 790 |
| Crime | 742 |
| Science Fiction | 534 |
| Horror | 519 |
| Fantasy | 504 |

### 5.3 原始语言分布（Top 5）

| 语言 | 数量 | 占比 |
|------|------|------|
| English (en) | 4505 | 93.8% |
| French (fr) | 70 | 1.5% |
| Spanish (es) | 32 | 0.7% |
| German (de) | 27 | 0.6% |
| Hindi (hi) | 19 | 0.4% |

---

## 6. 参考资料

1. [TMDB API Documentation](https://developers.themoviedb.org/3)
2. [Kaggle Dataset Page](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
3. [ISO 639-1 Language Codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
4. [ISO 3166-1 Country Codes](https://en.wikipedia.org/wiki/ISO_3166-1)

---

*文档创建日期: 2024年12月28日*
*数据集版本: TMDB 5000 Movie Dataset*
