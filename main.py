from enum import Enum
from typing import Dict, List, Set
from fastapi import FastAPI,Query
from pydantic import BaseModel,HttpUrl

# /docs will open the documentation (SwaggerUI)
# redoc will open the alternative documentation (automatic documentation)
# @something is called a decorator. like @app.get("/")
# all data validation is performed by Pydantic
# path operations are evaluated in order
# A request body is data sent from the client to the API, while the response body is the data sent from the API to the client.
# A request body can take more than one Pydantic model.
# if the parameter is declared in the path, it will be a path parameter, and if the paramter of type int,float,str, etc ... it will be declared as query, and if it is Pydantic model it will be in the request body.


#Image class
class Image(BaseModel):
    url:HttpUrl
    name:str

#This is an enum class
class Enums(str,Enum):
    greetings = "Hello world"
    potato = "Potato chips"

#item class
class Item(BaseModel):
    name:str
    description:str = None
    price:float
    tax:float = None
    tags: Set[str] = set()
    image:List[Image] = None

class Offer(BaseModel):
    name:str
    description:str
    price:float
    items:List[Item] = None
#This class will be added as-is to the output of the JSON schema for that model, and will be used in the API docs. You can use the same technique to extend the JSON schema to add extra info.
    class Config:
        schema_extra = {
            "example": {
                "name":"Foo",
                "description":"A very nice Item",
                "price":35.4,
                "tax": 3.2,

            }
        }


words_list = ["Burgers","Potato chips","Shawarma"]





app = FastAPI()

#you should inherit from BaseModel to be used as json
class Word(BaseModel):
    text:str = ""
    capitalized:bool = False

#This is for the index page.
@app.get("/")
def index():
    return {"greetings":"Hello World!"}

#The path is /words/word, it has an optional query capitalized, and a path parameter word.
@app.get("/words/{word}")
def get_word(word:str, capitalized:bool = False):
    if capitalized:
        return {"Word": word.upper()}
    return {"Word":word}

@app.post("/words/{word_id}")
def post_word(word_id:int,word:Word):
    if word.capitalized:
        word.text =  word.text.upper()
    return {"Response":"A new word has been added","word_id":word_id, "word":word}

#using the predefined words in the enum class
@app.get("/words/predefinded/{word}")
def predefined_words(word:Enums):
    # if word == Enums.greetings:
    #     return {"The greetings is ":word}
    if word == Enums.potato:
        return {"The meal today is":word}
    if word.value == Enums.greetings.value:
        return {"Method":"Using the value way"}

#the right way to define a path operation with a file path
@app.get("/paths/{file_path:path}")
def get_file_path(path:str):
    return {"The file path":path}

#a path operation with an optional query parameter, which will be after ? in the url. will be always a string unless a data type is specified in the code.
#if there is no default value for the query parameter, it will be required not optional.
@app.get("/words")
def get_words_from_index(index:int = 0):
    return {"words":words_list[index:]}

#a path operation that contains a request body
@app.post('/items/')
def create_item(item:Item):
    return item

#a path operation with a request body and path parameter
@app.post("/items/{item_id}")
def add_an_item_with_id(item_id:int,item:Item):
    return {"Item ID":item_id, "Item":item}

#A path operation with some validations, like max_length, min_length, and a regular expression which are specific for strings. The query is optional as it has a default value
""" @app.get("/items/")
def get_item(q:str = Query(default=None, max_length=50,min_length=3,regex="^fixedquery$")):
    return q """

#A path operation with some validations. To make the query required using "Query", we use three dots for the default value. they are called ellipsis.
""" @app.get("/items/")
def get_item(q:str = Query(...,max_length= 30)):
    return q """

#passing a list of strings to the query parameter, using it in the url would be like this as an example: q = chips & q = shawarma. You can also specify a default value for the list if not provided.
#if you use it without Query, it will be interpreted as a request body.
#the query has some additional metadata like description, title, alias (the name of the query, you can use names even if they are not allowed names in python.). To declare that the parameter is deprecated, you can assign deperecated as True.
#to set exclude a query parameter from the automatic documentation systems, set include_in_schema to False
@app.get("/items/")
def get_items(q:List[str] = Query([], title= "Query list", description="This is the description of the query list",alias="List[str]", deprecated=True,min_length=6 )):
    return {"List of words":q}

#This will be counted as a request body, not a query.
""" @app.get("/items/")
def get_items(q:List[str] = None):
    return {"List of words":q} """


#this can also be used instead of using List[str] but it wont check about the type of the values.
"""@app.get("/items/")
def get_items(q:list = Query([])):
    return {"List of words":q}"""


#a path operation with an Offer object that has attributes of another pydantic model.
@app.post("/offers/")
def create_offer(offer:Offer):
    return offer

#a path operation with a dictionary in the body with specified types for the keys and values.Note: Json will accept only strings as the keys, and then they will be converted automatically.
@app.post("/index-weights/")
def create_index_weights(weights:Dict[int,float]):
    return weights


