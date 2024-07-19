# -*- coding: utf-8 -*-

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.pydantic_v1 import BaseModel, Field

social_media = "..."
outline = """
...
"""
focus_on = "..."
language = "..."

llm = ChatOpenAI(model="gpt-4o", temperature=1.0)

generate_content_prompt = ChatPromptTemplate.from_template(
    "Based the outline: {outline} generate me a {social_media} post. Do not generate hashtags. Use {language} language. Be funny but professional"
)
correction_prompt = ChatPromptTemplate.from_template(
    "Correct this {social_media} post: {post}. Remove errors, unnecessary interjections and AIDA expressions. Add emojis. Do not change language"
)

class hashtag_generator(BaseModel):
    """Generates hashtags for a social media post."""

    hastags: list[str] = Field(..., description="A list of " + social_media + " hashtags. Focus mostly on " + focus_on)

def hashtags_to_string(hashtag_generator):
    result = ""
    for tag in hashtag_generator[0].hastags:
        result += "#" + tag + " "
    return result

tools = [hashtag_generator]
hashtags_chain = llm.bind_tools(tools) | PydanticToolsParser(tools=tools) | RunnableLambda(hashtags_to_string)

output_parser = StrOutputParser()
generate_content_chain = generate_content_prompt | llm | output_parser
correction_chain = correction_prompt | llm | output_parser

chain = (
    generate_content_chain
    | (lambda input: {"post": input, "social_media": social_media})
    | correction_chain
    | RunnableParallel(post = RunnablePassthrough(), hashtags = hashtags_chain)
)

result = chain.invoke({"outline": outline, "social_media": social_media, "language": language})
print(result["post"])
print(result["hashtags"])
