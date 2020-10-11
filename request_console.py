# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 22:03:07 2020

@author: codyf
"""

import requests
from bs4 import BeautifulSoup as html_parser
import sys

#Presentation. Delivers console, loops for input, and calls the 
#interpreter on the command.

class Console:
    def __init__(self):
        self.command = []
        self.interpreter = Interpreter()
        
    
    
    def loop(self):
        while True:
            self.command = input(":>").split()
            self.interpreter.call(self.command)
            

#Object responsible for interpreting the users input as a command and
#invoking the relevant object.
#The vocabulary attribute is a dictionary containing references to each
# command object.            
#The interpreter is responsible for holding state by instantiating their objects.
#state[0] = request state, [1] = response state, [2] = session state.

            
class Interpreter:
    def __init__(self):
        self.state = [RequestState(), ResponseState()]
        self.vocabulary = {"set" : SetCMD(),
                           "quit" : QuitCMD(),
                           "show" : ShowCMD(),
                           "get" : GetCMD()
                           }    


    
    def call(self, command):
        try:
            self.interpret(command)
        except Exception as e:
            print(e)
                
    def interpret(self, command):
        if command[0] not in self.vocabulary.keys():
            print("invalid syntax.")
        else:
            try:
                self.vocabulary[command[0]].call(command, self.state)
            except Exception as e:
                    print(e)
                    


# Command objects. Each command is denoted by CMD in the name.
# Each command has a call function to be referenced by outside objects.
# Command objects contain paramaters to validate whether the command syntax is
# correct or not.
#                    


#command for setting request and runtime paramters.                    
class SetCMD:
    def __init__(self):
        self.name = "set"
        self.desc = "Set the value of a paramter."
        #list of acceptable paramters for command validation
        self.parameters = ["request"] 

                
    def validate(self, command, state):
        if command[1] not in self.parameters:
            return False
        elif command[2] not in state[0].parameters.keys():
            return False
        else:
            return True

    def call(self, command, state):
        if self.validate(command, state) == False:
            print("syntax error.")
        else:
            try:
                state[0].parameters[command[2]] = command[3]
            except KeyError:
                print("request has no paramater %s" %command[2])

#command for exiting the program.            
class QuitCMD:
    def __init__(self):
        self.name = "quit"
        self.desc = "Exit Request Console."
        self.parameters = None


    def call(self, command, state):
        sys.exit()



class ShowCMD:
    def __init__(self):
        self.name = "show"
        self.desc = "show a parameter."
        self.parameters = ["request", "response"]


    def validate(self, command):
        if command[1] in self.parameters:
            return True

    def call(self, command, state):
        if self.validate(command) == False:
            print("syntax error.")
        else:
            if command[1] == "request":
                if len(command) == 2:
                    for k, v in state[0].parameters.items():
                        print(f"{k} : {v}")
                    
                elif len(command) == 3:
                    try:
                        print(command[2] + ":  " + state[0].parameters[command[2]])
                    except KeyError:
                        print(f"request has no parameter {command[2]}")
                        
                else:
                    print("no lol")
            
            elif command[1] == "response":
                if len(command) == 2:
                    print(f"{state[1].parameters['text']}")


class GetCMD:
    def __init__(self):
        self.name = "get"
        self.desc = "perform a get request."
        

    def validate(self, command):
        pass
        
    def prepare_request(self):
        prepared_request = {}
        for k, v in console.interpreter.state[0].parameters.items():
            if v:
                prepared_request[k] = v
        return(prepared_request)
        

    def update(self, response):
        console.interpreter.state[1].parameters["text"] = html_parser(response.text, features="lxml")
    
    def call(self, command, state):
        prepared_request = self.prepare_request()
        response = requests.get(**prepared_request)
        self.update(response)
        

class PostCMD:
    pass

class ClearCMD:
    pass

class EditCMD:
    pass


            
class RequestState:
    def __init__(self):
        self.parameters = {
            "url" : "http://example.com", 
            "cookies" : [],
            "headers" : "",
            "username" : "",
            "password" : "",
            "api_key" : "",
            "user-agent-string" : ""
            }

        self.session = requests.Session()


class ResponseState:
    def __init__(self):
        self.parameters = {   
            "url" : "",
            "cookies" : "",
            "headers" : {},
            "text" : "No response has been set. Have you run a request?",
            "cert" : "",
            "status" : int,
            "links" : [],
            "forms" : [],
            }

        
if __name__ == "__main__":
    console = Console()
    console.loop()