import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
from api.crud_requirements import get_all_requirements, get_requirement_by_id, add_requirement, update_requirement, delete_requirement
from api.crud_tests import get_all_tests, get_test_by_id, add_test, update_test, delete_test


model_name = os.environ["OPENROUTER_MODEL_NAME"]
api_key = os.environ["OPENROUTER_API_KEY"]

system_prompt = "Ты лид QA с опытом более 5 лет."

model = ChatOpenRouter(
    model_name=model_name,
    api_key=api_key
    )


messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content="Обнаружен дефект: удаление товара из корзины не обновляет стоимость всей корзины"),
    HumanMessage(content="Создай тест-план для проверки исправления этого дефекта"),
    HumanMessage(content="Используй требования и тестовые сценарии")
]

def ask_model(model: ChatOpenRouter, messages: list):
   agent = create_agent(
       model=model,
       tools=[get_all_requirements, get_requirement_by_id, add_requirement, update_requirement,
              delete_requirement, get_all_tests, get_test_by_id, add_test, update_test, delete_test])

   result = agent.invoke({"messages": messages})
   return result

def main():
    model_response = ask_model(model=model, messages=messages)
    ...
    

if __name__ == "__main__":
    main()