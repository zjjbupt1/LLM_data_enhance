from vector_search_module.utils.load_datasets import load_datasets
from vector_search_module.utils.load_models import load_embedding_model
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import (
    DistanceStrategy,
    maximal_marginal_relevance,
)

def generate_vector_db(vector_db_type:str, embedding_model_name: str, dataset_name: str, vector_index_path = "vectors/vector_db.index", distance_strategy = "EUCLIDEAN_DISTANCE"):
    """
    词嵌入向量库生成模块, 默认使用 faiss 作为向量数据库

    使用指定的词嵌入模型和数据集生成向量库，并保存到指定路径
    支持的嵌入向量数据库类型：
        faiss
        chroma
    
    其中,使用 faiss 向量数据库时，支持以下相似度计算策略：
        • 欧氏距离（EUCLIDEAN_DISTANCE）
        • 内积最大值（MAX_INNER_PRODUCT）
        • 点积（DOT_PRODUCT）
        • Jaccard相似度（JACCARD）
        • 余弦相似度（COSINE）
    支持的词嵌入模型：
        "uae": "./UAE-Large-V1",
        "azure-text-embedding-ada": "text-embedding-ada-002"

    支持的数据集：
        "anli" : ["ANLI/anli_v1.0/R1/test.jsonl", "ANLI/anli_v1.0/R2/test.jsonl", "ANLI/anli_v1.0/R3/test.jsonl"],
        "aqua" : "AQuA/test.json",
        "boolq" : "BoolQ/dev.jsonl",
        "factck" : "FactCK/test.jsonl",
        "obqa" : "OBQA/OpenBookQA-V1-Sep2018/Data/Main/test.jsonl",
        "gsm8k" : "gsm8k.jsonl",
        "logiqa" : "logiqa.jsonl"
    """
    # 加载数据集
    try:
        docs = load_datasets(dataset_name)
    except Exception as e:
        raise Exception(f"加载数据集失败，原因：{e}")

    # 加载词嵌入模型
    try:
        embeddings = load_embedding_model(embedding_model_name)
    except Exception as e:
        raise Exception(f"加载词嵌入模型失败，原因：{e}")

    # 生成向量库
    vector_index_path = f"{vector_index_path}.{vector_db_type}"
    if vector_db_type == "faiss" :
        db = FAISS.from_documents(docs, embeddings, distance_strategy=distance_strategy)
        db.save_local(vector_index_path)
    if vector_db_type == "chroma":
        db = Chroma.from_documents(docs, embeddings,persist_directory=vector_index_path)
    print(f"词嵌入向量库生成完毕，存储位置：{vector_index_path}")
    return db

def load_local_vectors_db(vector_db_type: str, vector_index_path: str, embedding_model_name: str, distance_strategy="EUCLIDEAN_DISTANCE"):
    """
    从本地加载向量库并返回向量库对象。

    参数：
        - vector_db_type: 向量库类型，支持"faiss"和"chroma"。
        - vector_index_path: 本地向量库路径。
        - embedding_model_name: 词嵌入模型名称。
        - distance_strategy : 使用 faiss 向量数据库时，支持以下相似度计算策略：
            • 欧氏距离（EUCLIDEAN_DISTANCE）
            • 内积最大值（MAX_INNER_PRODUCT）
            • 点积（DOT_PRODUCT）
            • Jaccard相似度（JACCARD）
            • 余弦相似度（COSINE）

    返回：
        - 向量库对象，可以是FAISS或Chroma的实例。
    """
    try:
        embedding = load_embedding_model(embedding_model_name)
    except Exception as e:
        raise Exception(f"加载词嵌入模型失败，原因：{e}")

    if vector_index_path[-1] == "/":
        vector_index_path = vector_index_path[:-1]
    if not vector_index_path.endswith(f"{vector_db_type}"):
        vector_index_path = f"{vector_index_path}.{vector_db_type}"
    if vector_db_type == "faiss" :
        db = FAISS.load_local(vector_index_path, embedding, normalize_L2=False ,distance_strategy = distance_strategy)
        # db = FAISS.load_local(vector_index_path, embedding, normalize_L2=False)
    if vector_db_type == "chroma":
        db = Chroma(persist_directory=vector_index_path,embedding_function=embedding)
    return db

def vector_db_search(db, query, top_k=3):
    """
    在向量库中执行查询并返回相似度最高的前k个结果。

    参数：
        - db: 向量库对象，可以是FAISS或Chroma的实例。
        - query: 查询字符串或文本。
        - top_k: 返回的相似度最高的前k个结果，默认为3。

    返回：
        - 结果列表，每个结果包含文档的索引、文档的相似度得分以及文档内容。
    """
    if db == None:
        raise Exception("向量库未初始化")
    results = db.similarity_search_with_score(query, top_k)
    return results

if __name__ == "__main__":
    # 指定模型、数据集和向量库路径
    vector_db_type = "faiss"
    model_name = "azure-text-embedding-ada"
    dataset_name = "anli"
    vector_index_path = "vectors/azure_anli_vector_db.index"

    # 生成向量库
    generate_vector_db(vector_db_type, model_name, dataset_name, vector_index_path) 
    db = load_local_vectors_db(vector_db_type,vector_index_path=vector_index_path,embedding_model_name=model_name)
    query = "this is a test string"
    top_k = 3
    print(vector_db_search(db, query, top_k))
