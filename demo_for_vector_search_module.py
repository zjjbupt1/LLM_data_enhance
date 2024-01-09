from vector_search_module.utils.embedding_vector_db import *

# 指定向量库类型、词嵌入模型和数据集
vector_db_type = "faiss"  # 支持"faiss"和"chroma"
embedding_model_name = "azure-text-embedding-ada" #使用AZURE时需要在环境变量中实现配置AZURE_OPENAI_KEY和AZURE_OPENAI_ENDPOINT
dataset_name = "logiqa"     # 选择一种支持的数据集
vector_index_path = "vector_search_module/vectors/azure_logiqa_vector_db.index" # 生成后的向量数据集本地存储地址

# 生成向量库并保存到指定路径
# generate_vector_db(vector_db_type, embedding_model_name, dataset_name, vector_index_path)

# 加载本地向量库
db = load_local_vectors_db(vector_db_type, vector_index_path, embedding_model_name)

# 执行相似度检索
query = "this is a test string"
top_k = 3 # 返回的相似度最高的前k个结果

results = vector_db_search(db, query, top_k)

# 输出检索结果
for index, result in enumerate(results):
    print(f"索引: {index} 文档内容: {result[0].page_content}, 相似度得分: {result[1]}, 文档元信息: {result[0].metadata}")
