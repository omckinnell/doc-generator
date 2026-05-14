def read_uploaded_file(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8")

def inject_docs_into_code(code: str, doc) -> str:
    lines = code.split("\n")
    result = []
    fn_names = {fn.name: fn for fn in doc.functions}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        
        # Check if this line is a function definition
        if stripped.startswith("def "):
            fn_name = stripped.split("(")[0].replace("def ", "").strip()
            
            if fn_name in fn_names:
                fn = fn_names[fn_name]
                
                # Build the docstring
                params_text = "\n".join([f"{indent}        {p}" for p in fn.parameters])
                docstring = (
                    f'{indent}    """\n'
                    f'{indent}    {fn.description}\n\n'
                    f'{indent}    Args:\n'
                    f'{params_text}\n\n'
                    f'{indent}    Returns:\n'
                    f'{indent}        {fn.returns}\n\n'
                    f'{indent}    Example:\n'
                    f'{indent}        {fn.example}\n'
                    f'{indent}    """\n'
                )
                
                result.append(line)  # the def line itself
                i += 1
                
                # Skip any existing docstring
                if i < len(lines) and '"""' in lines[i]:
                    while i < len(lines) and '"""' not in lines[i][lines[i].index('"""')+3:]:
                        i += 1
                    i += 1
                
                result.append(docstring)
                continue
        
        result.append(line)
        i += 1
    
    return "\n".join(result)


def to_markdown(doc) -> str:
    md = f"# Module Documentation\n\n"
    md += f"## Summary\n{doc.module_summary}\n\n"
    
    if doc.dependencies:
        md += f"## Dependencies\n"
        for dep in doc.dependencies:
            md += f"- `{dep}`\n"
        md += "\n"
    
    md += f"## Functions\n\n"
    for fn in doc.functions:
        md += f"### `{fn.name}`\n"
        md += f"{fn.description}\n\n"
        md += f"**Parameters:**\n"
        for param in fn.parameters:
            md += f"- {param}\n"
        md += f"\n**Returns:** {fn.returns}\n\n"
        md += f"**Example:**\n```python\n{fn.example}\n```\n\n"
    
    if doc.notes:
        md += f"## Notes\n{doc.notes}\n"
    
    return md