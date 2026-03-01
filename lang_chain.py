import os
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
from api.crud_requirements import get_all_requirements, get_requirement_by_id, add_requirement, update_requirement, delete_requirement
from api.crud_tests import get_all_tests, get_test_by_id, add_test, update_test, delete_test


model_name = os.environ["OPENROUTER_MODEL_NAME"]
api_key = os.environ["OPENROUTER_API_KEY"]

system_prompt = "Ты лид QA с опытом более 5 лет."

model = ChatOpenRouter(
    model_name=model_name,
    )

tooled_model = model.bind_tools([get_all_requirements, get_requirement_by_id, add_requirement, update_requirement, delete_requirement, get_all_tests, get_test_by_id, add_test, update_test, delete_test])

def pr(model: ChatOpenRouter):
   messages = [
    ("system", system_prompt),
    ("human", "Создай тест план для требовании №1 и №2")
]
   result = model.invoke(messages)
   return result

def main():
    result = pr(model=tooled_model)

if __name__ == "__main__":
    main()