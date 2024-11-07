from rag_interface.Rag import RAG
from repository.Repository import Repository
from llm_interface.LLM import LLM


class Core:

    def __init__(self) -> None:
        # initialize params
        # connect to db
        # perform query retrieval

        pass

    def core_impl(self, user_query):
        # take in user query
        # build rag if not built
        # get similar queries (rag)
        # pass the query to repo
        # get the data from db
        # pass both query and data to the llm
        # return the response to the user.
        rag_interface = RAG()
        most_relavant_query = rag_interface.retrieve(user_query)
        print(most_relavant_query)
        repository = Repository()
        patient_information = repository.retrieve_info(most_relavant_query)
        patient_info = ""
        for element in patient_information:
            for key in element:
                patient_info += str(key) + " : " + str(element[key]) + "\n"

        llm = LLM()
        resp = llm.chat_with_model(
            user_query=user_query, patient_information=patient_info
        )

        return resp

        # pass


# docker pull mysql/mysql-server

# docker run --name=<any container name> -d mysql/mysql-server

# docker logs <container name provided above> 2>&1 | grep GENERATED (this will printout the root's password)

# docker exec -it hruday-sql-native mysql -u"root" -p"password printed in the above command"

# GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '' WITH GRANT OPTION;
# FLUSH PRIVILEGES;

# &o=VoghS/1T1
# EJR*nz8%C@6VqE.G#4_,6,662aQzoR5M
# Cw?:8=8MM.Cd+2KoNn7D:Yd1k.018Vm^

# ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';
# CREATE USER 'root'@'%' IDENTIFIED BY 'your_new_password';
# GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
# FLUSH PRIVILEGES;
