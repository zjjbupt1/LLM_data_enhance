from langchain_community.docstore.document import Document
import jsonlines
import os

supported_datasets_dict = {
    "anli" : ["ANLI/anli_v1.0/R1/test.jsonl", "ANLI/anli_v1.0/R2/test.jsonl", "ANLI/anli_v1.0/R3/test.jsonl"],
    "aqua" : "AQuA/test.json",
    "boolq" : "BoolQ/dev.jsonl",
    "factck" : "FactCK/test.jsonl",
    "obqa" : "OBQA/OpenBookQA-V1-Sep2018/Data/Main/test.jsonl",
    "gsm8k" : "gsm8k.jsonl",
    "logiqa" : "logiqa.jsonl"
}

def load_datasets(dataset_name, separators=['\n'], sentence_max_size=512, chunk_overlap=0, mode='elements'):
    """
    加载数据集，返回数据集中的query
    """
    if dataset_name  not in supported_datasets_dict.keys():
        raise Exception("暂未支持该数据集，请选择从以下数据集中选择：\n{supported_datasets_dict}")

    docs = []
    query_list = []
    if dataset_name == "anli":
        r1 = os.path.join("vector_search_module/datasets",supported_datasets_dict[dataset_name][0])
        r2 = os.path.join("vector_search_module/datasets",supported_datasets_dict[dataset_name][1])
        r3 = os.path.join("vector_search_module/datasets",supported_datasets_dict[dataset_name][2])
        for f in [r1, r2, r3]:
            if not os.path.exists(f):
                raise Exception(f"该数据集{f}目标文件不存在，请检查。")
        with jsonlines.open(r1, "r") as reader:
            for line in reader:
                query_list.append(line["hypothesis"])
        with jsonlines.open(r2, "r") as reader:
            for line in reader:
                query_list.append(line["hypothesis"])
        with jsonlines.open(r3, "r") as reader:
            for line in reader:
                query_list.append(line["hypothesis"])
    if dataset_name == "aqua" or dataset_name == "boolq" or dataset_name == "gsm8k":
        file_path =  os.path.join("vector_search_module/datasets",supported_datasets_dict[dataset_name])
        if not os.path.exists(file_path):
            raise Exception(f"该数据集{file_path}目标文件不存在，请检查。")

        with jsonlines.open(file_path, "r") as reader:
            for line in reader:
                query_list.append(line["question"]) 
    if dataset_name == "logiqa":
        file_path =  os.path.join("vector_search_module/datasets",supported_datasets_dict[dataset_name])
        if not os.path.exists(file_path):
            raise Exception(f"该数据集{file_path}目标文件不存在，请检查。")

        with jsonlines.open(file_path, "r") as reader:
            for line in reader:
                query_list.append(line["query"])
    if dataset_name == "factck":
        file_path =  os.path.join("vector_search_module/datasets",supported_datasets_dict[dataset_name])
        if not os.path.exists(file_path):
            raise Exception(f"该数据集{file_path}目标文件不存在，请检查。")
        with jsonlines.open(file_path, "r") as reader:
            for line in reader:
                annotations = line["annotations"]
                for annotation in annotations:
                    questions = annotation["questions"]
                    for question in questions:
                        query_list.append(question)
    if dataset_name == "obqa":
        file_path =  os.path.join("vector_search_module/datasets",supported_datasets_dict[dataset_name])
        if not os.path.exists(file_path):
            raise Exception(f"该数据集{file_path}目标文件不存在，请检查。")
        with jsonlines.open(file_path, "r") as reader:
            for line in reader:
                question = line["question"]
                query = question["stem"]
                query_list.append(query)
    for query in query_list:
        # 创建一个空的Document对象
        page_content = query
        metadata = {"dataset":dataset_name,"source": str(supported_datasets_dict[dataset_name])}
        doc = Document(page_content=page_content,metadata=metadata)
        docs.append(doc) 
    return docs

if __name__ == "__main__":
    docs = load_datasets("factck")
    print(docs)
