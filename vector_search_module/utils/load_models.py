import torch
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings
from typing import List, Tuple, Dict
import openai
import os

EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
#可选模型
embedding_model_dict = {
    "uae": "./UAE-Large-V1",
    "azure-text-embedding-ada": "text-embedding-ada-002"
}


def load_embedding_model(model_name="uae",device=None):
    """
    加载词嵌入模型
    可选模型: ["uae", ]
    默认模型: "uae"
    """
    if model_name not in embedding_model_dict.keys():
        raise Exception(f"暂未支持该模型，请选择从以下模型选择：{embedding_model_dict}")
    if model_name == "azure-text-embedding-ada":
        os.environ["OPENAI_API_TYPE"] = "azure"
        if os.getenv('AZURE_OPENAI_ENDPOINT') != None :
            os.environ["OPENAI_API_BASE"] = os.getenv('AZURE_OPENAI_ENDPOINT')
        else:
            raise Exception("请先在环境变量中设置有效的 AZURE_OPENAI_ENDPOINT")
        if os.getenv('AZURE_OPENAI_KEY') != None :
            os.environ["OPENAI_API_KEY"] = os.getenv('AZURE_OPENAI_KEY')
        else:
            raise Exception("请先在环境变量中设置有效的 AZURE_OPENAI_KEY")
        os.environ["OPENAI_API_VERSION"] = "2023-05-15"
        embeddings = OpenAIEmbeddings(
                deployment=embedding_model_dict['azure-text-embedding-ada'],
                model="text-embedding-ada-002",
                openai_api_base=os.getenv('OPENAI_API_BASE'),
                openai_api_type="azure",
            )
        return embeddings
         
    if device == None:
        device = EMBEDDING_DEVICE

    model_path = os.path.join("vector_search_module/models",embedding_model_dict[model_name])
    if not os.path.exists(model_path+"/model.safetensors"):
        print(f"本地模型不存在，即将开始下载模型到: {model_path}/model.safetensors")
        import requests
        url = 'http://arm.hiz.one:1100/UAE-Large-V1/model.safetensors'
        destination = model_path+"/model.safetensors"
        try:
            response = requests.get(url)
            with open(destination, 'wb') as file:
                file.write(response.content)
            print(f'文件已下载到 {destination}')
        except Exception as e:
            if os.path.exists(model_path+"/model.safetensors"):
                os.remove(model_path+"/model.safetensors")
            print(f"文件下载失败，请重新下载: {e}")
            os._exit(-1)

    try:
        embeddings = HuggingFaceEmbeddings(model_name=model_path, model_kwargs={'device': device})
    except Exception as e:
        raise Exception(f"词嵌入模型加载失败，原因：{e}")

    return embeddings 


if __name__ == "__main__": 
    #embeddings = load_embedding_model(model_name="azure-text-embedding-ada")
    #print(embedded_query)
    embeddings = load_embedding_model(model_name="uae")
    embedded_query = embeddings.embed_query("What was the name mentioned in the conversation?")
    print(len(embedded_query))
