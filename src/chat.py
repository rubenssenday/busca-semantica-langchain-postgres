from search import search
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_template(
    """
CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Responda de forma mais polida e completa possível e incluir na resposta somente o dado que foi pedido. Exemplo: A empresa foi fundadada em (ano), O faturamento da (empresa) foi de (valor) ou a junção das duas"
- Se a informação não estiver explicitamente no CONTEXTO, responda:
"Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""
)

llm = ChatOpenAI(model="gpt-5-nano")

chain = prompt | llm

def chat(question):
    results = search(question)
    context = "\n".join([doc.page_content for doc, score in results])
    response = chain.invoke({"context": context, "question": question})
    return response.content

if __name__ == "__main__":
    while True:
        question = input("Faça sua pergunta: ")
        if question.lower() == "sair":
            break
        response = chat(question)
        print(f"RESPOSTA: {response}")