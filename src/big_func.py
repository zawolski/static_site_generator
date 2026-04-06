from htmlnode import *
from textnode import *
from funcs import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    elder_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            split_block = block.split("\n")
            stich_block = ""
            for piece in split_block:
                stich_block += piece + " "
            stich_block = stich_block.strip()
            node_list = text_to_textnodes(stich_block)
            child_list = []
            for node in node_list:
                child_list.append(text_node_to_html_node(node))
            parent = ParentNode("p", child_list)
            elder_children.append(parent)
        if block_type == BlockType.HEADING:
            hash_count = 0
            for symbol in block:
                if symbol == "#":
                    hash_count += 1
                else:
                    break
            tag = f"h{hash_count}"
            block2 = block[hash_count:]
            split_block = block2.split("\n")
            stich_block = ""
            for piece in split_block:
                stich_block += piece + " "
            stich_block = stich_block.strip()
            node_list = text_to_textnodes(stich_block)
            child_list = []
            for node in node_list:
                child_list.append(text_node_to_html_node(node))
            parent = ParentNode(tag, child_list)
            elder_children.append(parent)
        if block_type == BlockType.CODE:
            split_block = block.split("\n")
            child_value = ""
            for i in range(1,len(split_block)-1):
                child_value += split_block[i] + "\n"
            child = LeafNode("code", child_value)
            parent = ParentNode("pre", [child])
            elder_children.append(parent)
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote = ""
            for line in lines:
                line = line[1:]
                quote += line
            if quote[0] == " ":
                quote = quote[1:]
            node_list = text_to_textnodes(quote)
            child_list = []
            for node in node_list:
                child_list.append(text_node_to_html_node(node))
            parent = ParentNode("blockquote", child_list)
            elder_children.append(parent)
        if block_type == BlockType.OLIST:
            pchild_list = []
            lines = block.split("\n")
            for line in lines:
                line = line[3:]
                node_list = text_to_textnodes(line)
                child_list = []
                for node in node_list:
                    child_list.append(text_node_to_html_node(node))
                parent = ParentNode("li", child_list)
                pchild_list.append(parent)
            pparent = ParentNode("ol", pchild_list)
            elder_children.append(pparent)
        if block_type == BlockType.ULIST:
            pchild_list = []
            lines = block.split("\n")
            for line in lines:
                line = line[2:]
                node_list = text_to_textnodes(line)
                child_list = []
                for node in node_list:
                    child_list.append(text_node_to_html_node(node))
                parent = ParentNode("li", child_list)
                pchild_list.append(parent)
            pparent = ParentNode("ul", pchild_list)
            elder_children.append(pparent)

    elder = ParentNode("div", elder_children)

    return elder