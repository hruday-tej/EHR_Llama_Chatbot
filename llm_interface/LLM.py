from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class LLM:
    def __init__(self) -> None:
        self.model = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.system_message = "You are an Expert and Intelligent AI Diagnostic Model"

    def format_user_query(self, user_query, patient_information):
        string = f"""user query : {user_query}\n
        **EHR records**: {patient_information}"""
        print(f"Here is the user inp ---> {string}")
        string = (
            "your job is to read the user query and the EHR records, and answer the user's query using the EHR records. All the answers must be answered strictly following the EHR records provided along with the query. "
            + string
        )
        return string

    def chat_with_model(self, user_query, patient_information):
        messages = [
            SystemMessage(content=self.system_message),
            HumanMessage(
                content=self.format_user_query(user_query, patient_information),
                # temperature=0,
            ),
        ]

        model_response = self.model.invoke(messages, temperature=0.6)
        return model_response.content
