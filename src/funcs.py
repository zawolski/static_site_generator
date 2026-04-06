from textnode import *
import re
from enum import Enum

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            words = node.text.split(delimiter)
            if len(words) % 2 == 0:
                raise Exception("invalid markdown syntax")
            cur_type = 1
            for word in words:
                if cur_type == 1:
                    add_type = TextType.PLAIN
                else:
                    add_type = text_type
                if word != "":
                    hold = TextNode(word, add_type)
                    new_nodes.append(hold)
                cur_type = (cur_type+1) % 2
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for image in images:
            delim = f"![{image[0]}]({image[1]})"
            split_text = text.split(delim,1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0],TextType.PLAIN))
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
            text = split_text[1]
        if text != "":
            new_nodes.append(TextNode(text,TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        links =  extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for link in links:
            delim = f"[{link[0]}]({link[1]})"
            split_text = text.split(delim,1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0],TextType.PLAIN))
            new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
            text = split_text[1]
        if text != "":
            new_nodes.append(TextNode(text,TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    node_list = [TextNode(text,TextType.PLAIN)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        clean_block = block.strip()
        if clean_block != "":
            clean_blocks.append(clean_block)
    return clean_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def block_to_block_type(block):
    hast_count = 0
    is_space = False
    for char in block:
        if char == "#":
            hast_count += 1
        else:
            if char == " ":
                is_space = True
            break
    if hast_count > 0 and hast_count < 7 and is_space:
        return BlockType.HEADING
    if block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE
    lines = block.split("\n")
    breaker = True
    for line in lines:
        if line[0] != ">":
            breaker = False
            break
    if breaker:
        return BlockType.QUOTE
    breaker = True
    for line in lines:
        if line[:2] != "- ":
            breaker = False
            break
    if breaker:
        return BlockType.ULIST
    breaker = True
    count = 1
    for line in lines:
        if count<10 and line[:2] != f"{count}.":
            breaker = False
            break
        count += 1
    if breaker and count <= 10:
        return BlockType.OLIST
    return BlockType.PARAGRAPH