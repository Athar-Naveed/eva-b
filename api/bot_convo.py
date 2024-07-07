# ----------------------
# Imports
# ----------------------
import os,aiml
from glob import glob
# from neo4py.neo4py import Graph


# ----------------------
# AIML code starts here
# ----------------------

class AIML:
    def __init__(self) -> None:
        """
        initialized EVA's AIML kernel, and storing all the information into the EVA's brain if not stored already, if it is stored, we'll be retrieving them only

        params:
        None is received in params

        return:
        None is returned
        """
        brain = "./brain/brain.dump"
        self.eva = aiml.Kernel()
        if os.path.exists(brain):
            print("Loading information from the EVA's brain")
            self.eva.loadBrain(brain)
        else:
            self.eva.bootstrap(learnFiles="../aiml/*.aiml",commands="LEARN AIML")
            print(f"Saving information in the EVA's brain: {brain}")
            self.eva.saveBrain(brain)
        

    def response_to_user(self,user_input:str)->str:
        """
        This function is used to get the response from EVA's AIML kernel based on the user input, that'll be stored in the Neo4j's database as an episodic memory.

        Args:
            user_input (str): the input received from the user through mobile app or any other source

        Returns:
            resp (str): the bot reponse will be stored in db and then it'll be returned
        """
        resp = self.eva.respond(user_input,"EVA")
        # --------------------
        # call to db for storing user_input, bot response and time of conversation
        # --------------------
        return resp