# 词嵌入向量库生成与检索模块

## 简介

​		该模块提供了一个用于生成词嵌入向量库并执行相似度检索的工具。可以选择使用FAISS或Chroma作为向量数据库类型，支持不同的词嵌入模型和数据集。以下是模块的主要功能和用法说明。

​		**支持的向量数据库类型：**faiss、chroma

​		**支持的词嵌入模型：**uae、azure-text-embedding-ada

​		**支持的数据集：**anli、aqua、boolq、factck、obqa、gsm8k、logiqa

## 使用方法

**需要在 vector_search_module 文件夹外部执行以下代码：**

### 1、生成向量库

```python
from vector_search_module.utils.embedding_vector_db import *

# 指定向量库类型、词嵌入模型和数据集
vector_db_type = "faiss"  # 支持"faiss"和"chroma"
embedding_model_name = "azure-text-embedding-ada" #使用AZURE时需要在环境变量中实现配置AZURE_OPENAI_KEY和AZURE_OPENAI_ENDPOINT
dataset_name = "logiqa"     # 选择一种支持的数据集
vector_index_path = "vector_search_module/vectors/azure_logiqa_vector_db.index" # 生成后的向量数据集本地存储地址

# 生成向量库并保存到指定路径
generate_vector_db(vector_db_type, embedding_model_name, dataset_name, vector_index_path)
```

### 2、加载本地向量库

```python
from vector_search_module.utils.embedding_vector_db import *

# 指定向量库类型、本地向量库路径、词嵌入模型和相似度计算策略
# 以下信息需要跟步骤1、生成向量库使用的信息保持一致
vector_db_type = "faiss"  # 支持"faiss"和"chroma"
embedding_model_name = "azure-text-embedding-ada"
vector_index_path = "vector_search_module/vectors/azure_logiqa_vector_db.index"

# 加载本地向量库
db = load_local_vectors_db(vector_db_type, vector_index_path, embedding_model_name)
```

### 3、执行相似度检索

```python
from vector_search_module.utils.embedding_vector_db import *

# 执行相似度检索
query = "this is a test string"
top_k = 3 # 返回的相似度最高的前k个结果

results = vector_db_search(db, query, top_k)

# 输出检索结果
for result in results:
    print(f"文档内容: {result[0].page_content}, 相似度得分: {result[1]}, 文档元信息: {result[0].metadata}")
```



## 注意事项

- 在使用前，请确保已安装依赖库，可以通过运行`pip install -r requirements.txt`来安装所需依赖。
- 请根据实际需求选择合适的向量数据库类型、词嵌入模型和数据集。
- 请确保本地向量库路径正确，并在加载时指定正确的向量数据库类型。
