class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplentedError("yall didn't implement this")

    def props_to_html(self):
        if self.props is None:
            return ""
        if len(self.props) == 0:
            return ""
        res = ""
        for item in self.props:
            res += " "
            res += item
            res += '="'
            res += self.props[item]
            res += '"'
        return res

    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaves need values")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nProps: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("yall need a tag")
        if self.children is None:
            raise ValueError("yall need some children")
        res = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            res += child.to_html()
        res += f"</{self.tag}>"
        return res