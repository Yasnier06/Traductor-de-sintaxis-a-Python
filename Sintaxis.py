import streamlit as st
import re
from datetime import datetime
import subprocess
import tempfile
import os
import sys
import shutil

# =========================
#   TRADUCTOR DE CÓDIGO
# =========================
class CodeTranslator:
    def __init__(self):
        self.translations = {
            # Python conversions
            ('python', 'cpp'): self.python_to_cpp,
            ('python', 'csharp'): self.python_to_csharp,
            ('python', 'java'): self.python_to_java,
            ('python', 'javascript'): self.python_to_javascript,
            ('python', 'ruby'): self.python_to_ruby,
            ('python', 'go'): self.python_to_go,
            ('python', 'rust'): self.python_to_rust,
            ('python', 'php'): self.python_to_php,
            ('python', 'typescript'): self.python_to_typescript,

            # C++ conversions
            ('cpp', 'python'): self.cpp_to_python,
            ('cpp', 'csharp'): self.cpp_to_csharp,
            ('cpp', 'java'): self.cpp_to_java,
            ('cpp', 'javascript'): self.cpp_to_javascript,
            ('cpp', 'ruby'): self.cpp_to_ruby,
            ('cpp', 'go'): self.cpp_to_go,
            ('cpp', 'rust'): self.cpp_to_rust,
            ('cpp', 'php'): self.cpp_to_php,
            ('cpp', 'typescript'): self.cpp_to_typescript,

            # C# conversions
            ('csharp', 'python'): self.csharp_to_python,
            ('csharp', 'cpp'): self.csharp_to_cpp,
            ('csharp', 'java'): self.java_to_csharp,
            ('csharp', 'javascript'): self.javascript_to_csharp,
            ('csharp', 'ruby'): self.ruby_to_csharp,
            ('csharp', 'go'): self.go_to_csharp,
            ('csharp', 'rust'): self.rust_to_csharp,
            ('csharp', 'php'): self.php_to_csharp,
            ('csharp', 'typescript'): self.typescript_to_csharp,

            # Java conversions
            ('java', 'python'): self.java_to_python,
            ('java', 'cpp'): self.java_to_cpp,
            ('java', 'csharp'): self.java_to_csharp,
            ('java', 'javascript'): self.java_to_javascript,
            ('java', 'ruby'): self.java_to_ruby,
            ('java', 'go'): self.java_to_go,
            ('java', 'rust'): self.java_to_rust,
            ('java', 'php'): self.java_to_php,
            ('java', 'typescript'): self.java_to_typescript,

            # JavaScript conversions
            ('javascript', 'python'): self.javascript_to_python,
            ('javascript', 'cpp'): self.javascript_to_cpp,
            ('javascript', 'csharp'): self.javascript_to_csharp,
            ('javascript', 'java'): self.javascript_to_java,
            ('javascript', 'ruby'): self.javascript_to_ruby,
            ('javascript', 'go'): self.javascript_to_go,
            ('javascript', 'rust'): self.javascript_to_rust,
            ('javascript', 'php'): self.javascript_to_php,
            ('javascript', 'typescript'): self.javascript_to_typescript,

            # Ruby conversions
            ('ruby', 'python'): self.ruby_to_python,
            ('ruby', 'cpp'): self.ruby_to_cpp,
            ('ruby', 'csharp'): self.ruby_to_csharp,
            ('ruby', 'java'): self.ruby_to_java,
            ('ruby', 'javascript'): self.ruby_to_javascript,
            ('ruby', 'go'): self.ruby_to_go,
            ('ruby', 'rust'): self.ruby_to_rust,
            ('ruby', 'php'): self.ruby_to_php,
            ('ruby', 'typescript'): self.ruby_to_typescript,

            # Go conversions
            ('go', 'python'): self.go_to_python,
            ('go', 'cpp'): self.go_to_cpp,
            ('go', 'csharp'): self.go_to_csharp,
            ('go', 'java'): self.go_to_java,
            ('go', 'javascript'): self.go_to_javascript,
            ('go', 'ruby'): self.go_to_ruby,
            ('go', 'rust'): self.go_to_rust,
            ('go', 'php'): self.go_to_php,
            ('go', 'typescript'): self.go_to_typescript,

            # Rust conversions
            ('rust', 'python'): self.rust_to_python,
            ('rust', 'cpp'): self.rust_to_cpp,
            ('rust', 'csharp'): self.rust_to_csharp,
            ('rust', 'java'): self.rust_to_java,
            ('rust', 'javascript'): self.rust_to_javascript,
            ('rust', 'ruby'): self.rust_to_ruby,
            ('rust', 'go'): self.rust_to_go,
            ('rust', 'php'): self.rust_to_php,
            ('rust', 'typescript'): self.rust_to_typescript,

            # PHP conversions
            ('php', 'python'): self.php_to_python,
            ('php', 'cpp'): self.php_to_cpp,
            ('php', 'csharp'): self.php_to_csharp,
            ('php', 'java'): self.php_to_java,
            ('php', 'javascript'): self.php_to_javascript,
            ('php', 'ruby'): self.php_to_ruby,
            ('php', 'go'): self.php_to_go,
            ('php', 'rust'): self.php_to_rust,
            ('php', 'typescript'): self.php_to_typescript,

            # TypeScript conversions
            ('typescript', 'python'): self.typescript_to_python,
            ('typescript', 'cpp'): self.typescript_to_cpp,
            ('typescript', 'csharp'): self.typescript_to_csharp,
            ('typescript', 'java'): self.typescript_to_java,
            ('typescript', 'javascript'): self.typescript_to_javascript,
            ('typescript', 'ruby'): self.typescript_to_ruby,
            ('typescript', 'go'): self.typescript_to_go,
            ('typescript', 'rust'): self.typescript_to_rust,
            ('typescript', 'php'): self.typescript_to_php,
        }

    def translate(self, code, from_lang, to_lang):
        if from_lang == to_lang:
            return code
        key = (from_lang, to_lang)
        if key in self.translations:
            return self.translations[key](code)
        return "Traducción no disponible para esta combinación de lenguajes."

    # ===================== PYTHON → C++ =====================
    def python_to_cpp(self, code):
        result = [
            "#include <iostream>",
            "#include <string>",
            "using namespace std;",
            "",
            "int main() {"
        ]
        lines = code.strip().split('\n')
        indent_unit = "    "
        indent_level = 1
        block_count = 0

        def cur_indent():
            return indent_unit * indent_level

        for raw_line in lines:
            line = raw_line.rstrip()
            stripped = line.strip()
            if not stripped:
                continue

            # int(input(""))
            m_int_in = re.match(r'(\w+)\s*=\s*int\s*$$\s*input\s*$$\s*(["\'])(.*?)\2\s*$$\s*$$', stripped)
            if m_int_in:
                var = m_int_in.group(1)
                prompt = m_int_in.group(3)
                result.append(f'{cur_indent()}int {var};')
                result.append(f'{cur_indent()}cout << "{prompt}: ";')
                result.append(f'{cur_indent()}cin >> {var};')
                result.append(f'{cur_indent()}cin.ignore();')
                continue

            # input("")
            m_input = re.match(r'(\w+)\s*=\s*input\s*$$\s*(["\'])(.*?)\2\s*$$', stripped)
            if m_input:
                var = m_input.group(1)
                prompt = m_input.group(3)
                result.append(f'{cur_indent()}string {var};')
                result.append(f'{cur_indent()}cout << "{prompt}: ";')
                result.append(f'{cur_indent()}getline(cin, {var});')
                continue

            # f-string print
            m_fprint = re.match(r'print\s*$$\s*f(["\'])(.*?)\1\s*$$', stripped)
            if m_fprint:
                fcontent = m_fprint.group(2)
                parts = re.split(r'\{([^}]+)\}', fcontent)
                cout_parts = []
                for i, p in enumerate(parts):
                    if i % 2 == 0:
                        if p:
                            p_escaped = p.replace('"', r'\"')
                            cout_parts.append(f'"{p_escaped}"')
                    else:
                        cout_parts.append(p.strip())
                cout_line = ' << '.join(cout_parts) + ' << endl;'
                result.append(f'{cur_indent()}cout << {cout_line}')
                continue

            # print
            m_print = re.match(r'print\s*$$\s*(.*?)\s*$$', stripped)
            if m_print:
                arg = m_print.group(1)
                result.append(f'{cur_indent()}cout << {arg} << endl;')
                continue

            # if/elif/else
            if stripped.startswith('if ') and stripped.endswith(':'):
                cond = stripped[3:-1].strip()
                result.append(f'{cur_indent()}if ({cond}) {{')
                indent_level += 1
                block_count += 1
                continue

            if stripped.startswith('elif ') and stripped.endswith(':'):
                cond = stripped[5:-1].strip()
                indent_level -= 1
                result.append(f'{cur_indent()}}} else if ({cond}) {{')
                indent_level += 1
                continue

            if stripped.startswith('else:'):
                indent_level -= 1
                result.append(f'{cur_indent()}}} else {{')
                indent_level += 1
                continue

            # for
            m_for2 = re.match(r'for\s+(\w+)\s+in\s+range\s*$$\s*(\d+)\s*,\s*(\d+)\s*$$:', stripped)
            m_for1 = re.match(r'for\s+(\w+)\s+in\s+range\s*$$\s*(\d+)\s*$$:', stripped)
            if m_for2:
                v, a, b = m_for2.groups()
                result.append(f'{cur_indent()}for (int {v} = {a}; {v} < {b}; {v}++) {{')
                indent_level += 1
                block_count += 1
                continue

            if m_for1:
                v, lim = m_for1.groups()
                result.append(f'{cur_indent()}for (int {v} = 0; {v} < {lim}; {v}++) {{')
                indent_level += 1
                block_count += 1
                continue

            # while
            if stripped.startswith('while ') and stripped.endswith(':'):
                cond = stripped[6:-1].strip()
                result.append(f'{cur_indent()}while ({cond}) {{')
                indent_level += 1
                block_count += 1
                continue

            # assignment
            if '=' in stripped and not any(stripped.startswith(k)
                                           for k in ['if', 'elif', 'else', 'for', 'while', 'print', 'return']):
                var, val = stripped.split('=', 1)
                var = var.strip()
                val = val.strip()

                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    result.append(f'{cur_indent()}string {var} = {val};')
                elif re.match(r'^-?\d+\.\d+$', val):
                    result.append(f'{cur_indent()}double {var} = {val};')
                elif re.match(r'^-?\d+$', val):
                    result.append(f'{cur_indent()}int {var} = {val};')
                else:
                    result.append(f'{cur_indent()}auto {var} = {val};')
                continue

            result.append(f'{cur_indent()}// {stripped}')

        while block_count > 0:
            indent_level -= 1
            result.append(f'{cur_indent()}}}')
            block_count -= 1

        result.append(f'    return 0;')
        result.append('}')
        return '\n'.join(result)

    def python_to_csharp(self, code):
        result = ["using System;", "", "class Program", "{", "    static void Main()", "    {"]
        for line in code.strip().split('\n'):
            stripped = line.strip()
            if stripped.startswith('print('):
                m = re.match(r'print\s*$$\s*(.*?)\s*$$', stripped)
                if m:
                    arg = m.group(1)
                    result.append(f'        Console.WriteLine({arg});')
        result += ["    }", "}"]
        return '\n'.join(result)

    def python_to_java(self, code):
        lines = code.strip().split('\n')
        out = ["import java.util.Scanner;","","public class Main {","    public static void main(String[] args) {","        Scanner scanner = new Scanner(System.in);"]
        indent_level = 1
        indent_unit = "        "
        declared_vars = set()
        
        def get_indent():
            return indent_unit * indent_level
        
        for raw in lines:
            s = raw.strip()
            if not s:
                out.append("")
                continue
            
            # Calcular nivel de indentación basado en espacios iniciales
            leading_spaces = len(raw) - len(raw.lstrip())
            current_indent = leading_spaces // 4  # Asumiendo indentación de 4 espacios
            
            # Ajustar indent_level si hay cambio
            if current_indent < indent_level:
                while indent_level > current_indent:
                    indent_level -= 1
                    out.append(get_indent() + '}')
            
            # print(...) or print $$ ... $$
            m = re.match(r'^print\s*$$\s*(.*?)\s*$$\s*$', s)
            if not m:
                m = re.match(r'^print\s*\((.*)\)\s*$', s)
            if m:
                arg = m.group(1)
                out.append(f'{get_indent()}System.out.println({arg});')
                continue
            
            # var = int(input()) or var = int(input("prompt")) or int $$ input $$ "prompt" $$ $$
            m_int_in = re.match(r'^(\w+)\s*=\s*int\s*$$\s*input\s*$$\s*(["\'])(.*?)\2\s*$$\s*$$\s*$', s)
            if not m_int_in:
                m_int_in = re.match(r'^(\w+)\s*=\s*int\s*\(\s*input\s*\(\s*(?:["\'](.*?)["\'])?\s*\)\s*\)\s*$', s)
                if m_int_in:
                    var = m_int_in.group(1)
                    prompt = m_int_in.group(2) or "" if len(m_int_in.groups()) > 1 else ""
                    if prompt:
                        out.append(f'{get_indent()}System.out.print("{prompt}");')
                    out.append(f'{get_indent()}int {var} = Integer.parseInt(scanner.nextLine());')
                    declared_vars.add(var)
                    continue
            else:
                var = m_int_in.group(1)
                prompt = m_int_in.group(3) or ""
                if prompt:
                    out.append(f'{get_indent()}System.out.print("{prompt}");')
                out.append(f'{get_indent()}int {var} = Integer.parseInt(scanner.nextLine());')
                declared_vars.add(var)
                continue
            
            # var = input() or var = input("prompt") or input $$ "prompt" $$
            m_in = re.match(r'^(\w+)\s*=\s*input\s*$$\s*(["\'])(.*?)\2\s*$$\s*$', s)
            if not m_in:
                m_in = re.match(r'^(\w+)\s*=\s*input\s*\(\s*(?:["\'](.*?)["\'])?\s*\)\s*$', s)
                if m_in:
                    var = m_in.group(1)
                    prompt = m_in.group(2) or "" if len(m_in.groups()) > 1 else ""
                    if prompt:
                        out.append(f'{get_indent()}System.out.print("{prompt}");')
                    out.append(f'{get_indent()}String {var} = scanner.nextLine();')
                    declared_vars.add(var)
                    continue
            else:
                var = m_in.group(1)
                prompt = m_in.group(3) or ""
                if prompt:
                    out.append(f'{get_indent()}System.out.print("{prompt}");')
                out.append(f'{get_indent()}String {var} = scanner.nextLine();')
                declared_vars.add(var)
                continue
            
            # if/elif/else/while/for
            if s.endswith(":"):
                header = s[:-1].strip()
                
                # if con $$ o con paréntesis normales
                m_if = re.match(r'^if\s*$$\s*(.*?)\s*$$\s*$', header)
                if m_if:
                    cond = m_if.group(1).strip()
                    out.append(f'{get_indent()}if ({cond}) {{')
                    indent_level += 1
                    continue
                elif header.startswith('if '):
                    cond = header[3:].strip()
                    out.append(f'{get_indent()}if ({cond}) {{')
                    indent_level += 1
                    continue
                
                # elif con $$ o con paréntesis normales
                m_elif = re.match(r'^elif\s*$$\s*(.*?)\s*$$\s*$', header)
                if m_elif:
                    cond = m_elif.group(1).strip()
                    indent_level -= 1
                    out.append(get_indent() + '}')
                    out.append(f'{get_indent()}else if ({cond}) {{')
                    indent_level += 1
                    continue
                elif header.startswith('elif '):
                    cond = header[5:].strip()
                    indent_level -= 1
                    out.append(get_indent() + '}')
                    out.append(f'{get_indent()}else if ({cond}) {{')
                    indent_level += 1
                    continue
                
                # else
                elif header.startswith('else'):
                    indent_level -= 1
                    out.append(get_indent() + '}')
                    out.append(f'{get_indent()}else {{')
                    indent_level += 1
                    continue
                
                # while con $$ o con paréntesis normales
                m_while = re.match(r'^while\s*$$\s*(.*?)\s*$$\s*$', header)
                if m_while:
                    cond = m_while.group(1).strip()
                    out.append(f'{get_indent()}while ({cond}) {{')
                    indent_level += 1
                    continue
                elif header.startswith('while '):
                    cond = header[6:].strip()
                    out.append(f'{get_indent()}while ({cond}) {{')
                    indent_level += 1
                    continue
                
                # for loops - manejar tanto () como $$
                m_for = re.match(r'^for\s+(\w+)\s+in\s+range\s*$$\s*(\d+)\s*$$\s*$', header)
                if not m_for:
                    m_for = re.match(r'^for\s+(\w+)\s+in\s+range\s*\(\s*(\d+)\s*\)\s*$', header)
                if m_for:
                    v, lim = m_for.groups()
                    out.append(f'{get_indent()}for (int {v} = 0; {v} < {lim}; {v}++) {{')
                    declared_vars.add(v)
                    indent_level += 1
                    continue
                
                m_for2 = re.match(r'^for\s+(\w+)\s+in\s+range\s*$$\s*(\d+)\s*,\s*(\d+)\s*$$\s*$', header)
                if not m_for2:
                    m_for2 = re.match(r'^for\s+(\w+)\s+in\s+range\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*$', header)
                if m_for2:
                    v, a, b = m_for2.groups()
                    out.append(f'{get_indent()}for (int {v} = {a}; {v} < {b}; {v}++) {{')
                    declared_vars.add(v)
                    indent_level += 1
                    continue
            
            # assignment
            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', s)
            if m_assign:
                var, val = m_assign.groups()
                # Si la variable no está declarada, intentar inferir el tipo
                if var not in declared_vars:
                    # Inferir tipo básico
                    if re.match(r'^-?\d+$', val.strip()):
                        out.append(f'{get_indent()}int {var} = {val};')
                    elif re.match(r'^-?\d+\.\d+$', val.strip()):
                        out.append(f'{get_indent()}double {var} = {val};')
                    elif val.strip().startswith('"') or val.strip().startswith("'"):
                        out.append(f'{get_indent()}String {var} = {val};')
                    else:
                        out.append(f'{get_indent()}var {var} = {val};')
                    declared_vars.add(var)
                else:
                    out.append(f'{get_indent()}{var} = {val};')
                continue
            
            out.append(f'{get_indent()}// {s}')
        
        # Cerrar todos los bloques abiertos
        while indent_level > 1:
            indent_level -= 1
            out.append(get_indent() + '}')
        
        out.append('        scanner.close();')
        out.append('    }')
        out.append('}')
        return '\n'.join(out)

    def python_to_javascript(self, code):
        lines = code.strip().split('\n')
        out = ["const fs = require('fs');","const inputData = fs.readFileSync(0, 'utf8').split('\n');","let __input_idx = 0;","function input(){ return inputData[__input_idx++] || ''; }",""]
        for raw in lines:
            s = raw.strip()
            if not s:
                out.append("")
                continue
            m_print = re.match(r'^print\s*\((.*)\)\s*$', s)
            if m_print:
                arg = m_print.group(1)
                out.append(f'console.log({arg});')
                continue
            m_int_in = re.match(r'^(\w+)\s*=\s*int\s*\(\s*input\s*\(\s*\)\s*\)\s*$', s)
            if m_int_in:
                var = m_int_in.group(1)
                out.append(f'let {var} = parseInt(input());')
                continue
            m_in = re.match(r'^(\w+)\s*=\s*input\s*\(\s*\)\s*$', s)
            if m_in:
                var = m_in.group(1)
                out.append(f'let {var} = input();')
                continue
            m_for = re.match(r'^for\s+(\w+)\s+in\s+range\s*\(\s*(\d+)\s*\)\s*:$', s)
            if m_for:
                v, lim = m_for.groups()
                out.append(f'for (let {v} = 0; {v} < {lim}; {v}++) {{')
                continue
            if s.endswith(':'):
                hdr = s[:-1]
                if hdr.startswith('if '):
                    cond = hdr[3:]
                    out.append(f'if ({cond}) {{')
                    continue
                if hdr.startswith('elif '):
                    cond = hdr[5:]
                    out.append(f'else if ({cond}) {{')
                    continue
                if hdr.startswith('else'):
                    out.append('else {')
                    continue
            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', s)
            if m_assign:
                var, val = m_assign.groups()
                out.append(f'let {var} = {val};')
                continue
            out.append(f'// {s}')
        return '\n'.join(out)

    def python_to_ruby(self, code):
        lines = code.splitlines()
        out = []
        stack = []  # store indent levels for open blocks
        for raw in lines:
            indent = len(raw) - len(raw.lstrip(' '))
            s = raw.strip()

            # close blocks if indent decreased
            while stack and indent <= stack[-1]:
                stack.pop()
                out.append('end')

            if not s:
                out.append("")
                continue

            m_print = re.match(r'^print\s*\((.*)\)\s*$', s)
            if m_print:
                out.append(f'puts {m_print.group(1)}')
                continue

            m_int_in = re.match(r'^(\w+)\s*=\s*int\s*\(\s*input\s*\(\s*\)\s*\)\s*$', s)
            if m_int_in:
                out.append(f'{m_int_in.group(1)} = gets.chomp.to_i')
                continue

            m_in = re.match(r'^(\w+)\s*=\s*input\s*\(\s*\)\s*$', s)
            if m_in:
                out.append(f'{m_in.group(1)} = gets.chomp')
                continue

            m_for = re.match(r'^for\s+(\w+)\s+in\s+range\s*\(\s*(\d+)\s*\)\s*:$', s)
            if m_for:
                v, lim = m_for.groups()
                out.append(f'for {v} in 0...{lim}')
                stack.append(indent)
                continue

            if s.endswith(':'):
                hdr = s[:-1].strip()
                if hdr.startswith('if '):
                    cond = hdr[3:]
                    out.append(f'if {cond}')
                    stack.append(indent)
                    continue
                if hdr.startswith('elif '):
                    cond = hdr[5:]
                    out.append(f'elsif {cond}')
                    stack.append(indent)
                    continue
                if hdr.startswith('else'):
                    out.append('else')
                    stack.append(indent)
                    continue

            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', s)
            if m_assign:
                out.append(s)
                continue

            out.append(f'# {s}')

        # close any remaining blocks
        while stack:
            stack.pop()
            out.append('end')

        return '\n'.join(out)

    def python_to_go(self, code):
        lines = code.strip().split('\n')
        needs_bufio = any(re.search(r'input\s*\(', l) for l in lines)
        imports = ['fmt']
        if needs_bufio:
            imports = ['fmt','bufio','os','strings','strconv']
        out = ['package main','']
        if imports:
            out.append('import (')
            for im in imports:
                out.append(f'    "{im}"')
            out.append(')')
            out.append('')
        out.append('func main() {')
        if needs_bufio:
            out.append('    reader := bufio.NewReader(os.Stdin)')
        for raw in lines:
            s = raw.strip()
            if not s:
                out.append('')
                continue
            m_print = re.match(r'^print\s*\((.*)\)\s*$', s)
            if m_print:
                out.append(f'    fmt.Println({m_print.group(1)})')
                continue
            m_int_in = re.match(r'^(\w+)\s*=\s*int\s*\(\s*input\s*\(\s*\)\s*\)\s*$', s)
            if m_int_in:
                var = m_int_in.group(1)
                out.append(f"    {var}_str, _ := reader.ReadString('\\n')")
                out.append(f'    {var}_str = strings.TrimSpace({var}_str)')
                out.append(f'    var {var} int')
                out.append(f'    {var}, _ = strconv.Atoi({var}_str)')
                continue
            m_in = re.match(r'^(\w+)\s*=\s*input\s*\(\s*\)\s*$', s)
            if m_in:
                var = m_in.group(1)
                out.append(f"    {var}_str, _ := reader.ReadString('\\n')")
                out.append(f'    var {var} string')
                out.append(f'    {var} = strings.TrimSpace({var}_str)')
                continue
            m_for = re.match(r'^for\s+(\w+)\s+in\s+range\s*\(\s*(\d+)\s*\)\s*:$', s)
            if m_for:
                v, lim = m_for.groups()
                out.append(f'    for {v} := 0; {v} < {lim}; {v}++ {{')
                continue
            if s.endswith(':'):
                hdr = s[:-1]
                if hdr.startswith('if '):
                    cond = hdr[3:]
                    out.append(f'    if {cond} {{')
                    continue
            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', s)
            if m_assign:
                out.append(f'    {s}')
                continue
            out.append(f'    // {s}')
        out.append('}')
        return '\n'.join(out)

    def python_to_rust(self, code):
        lines = code.strip().split('\n')
        out = ['use std::io;','use std::io::Write;','','fn main() {']
        for raw in lines:
            s = raw.strip()
            if not s:
                out.append('')
                continue
            m_print = re.match(r'^print\s*\((.*)\)\s*$', s)
            if m_print:
                out.append(f'    println!("{{}}", {m_print.group(1)});')
                continue
            m_int_in = re.match(r'^(\w+)\s*=\s*int\s*\(\s*input\s*\(\s*\)\s*\)\s*$', s)
            if m_int_in:
                var = m_int_in.group(1)
                out.append(f'    let mut {var}_s = String::new();')
                out.append(f'    io::stdin().read_line(&mut {var}_s).expect("read failed");')
                out.append(f'    let {var}: i32 = {var}_s.trim().parse().unwrap_or(0);')
                continue
            m_in = re.match(r'^(\w+)\s*=\s*input\s*\(\s*\)\s*$', s)
            if m_in:
                var = m_in.group(1)
                out.append(f'    let mut {var} = String::new();')
                out.append(f'    io::stdin().read_line(&mut {var}).expect("read failed");')
                out.append(f'    let {var} = {var}.trim().to_string();')
                continue
            m_for = re.match(r'^for\s+(\w+)\s+in\s+range\s*\(\s*(\d+)\s*\)\s*:$', s)
            if m_for:
                v, lim = m_for.groups()
                out.append(f'    for {v} in 0..{lim} {{')
                continue
            if s.endswith(':'):
                hdr = s[:-1]
                if hdr.startswith('if '):
                    cond = hdr[3:]
                    out.append(f'    if {cond} {{')
                    continue
            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', s)
            if m_assign:
                out.append(f'    // assignment: {s}')
                continue
            out.append(f'    // {s}')
        out.append('}')
        return '\n'.join(out)

    def python_to_php(self, code):
        lines = code.strip().split('\n')
        out = ['<?php']
        for raw in lines:
            s = raw.strip()
            if not s:
                out.append('')
                continue
            m_print = re.match(r'^print\s*\((.*)\)\s*$', s)
            if m_print:
                out.append(f'echo {m_print.group(1)} . "\\n";')
                continue
            m_int_in = re.match(r'^(\w+)\s*=\s*int\s*\(\s*input\s*\(\s*\)\s*\)\s*$', s)
            if m_int_in:
                var = m_int_in.group(1)
                out.append(f'${var} = (int)trim(fgets(STDIN));')
                continue
            m_in = re.match(r'^(\w+)\s*=\s*input\s*\(\s*\)\s*$', s)
            if m_in:
                var = m_in.group(1)
                out.append(f'${var} = trim(fgets(STDIN));')
                continue
            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', s)
            if m_assign:
                var, val = m_assign.groups()
                out.append(f'${var} = {val};')
                continue
            out.append(f'// {s}')
        out.append('?>')
        return '\n'.join(out)

    def python_to_typescript(self, code):
        lines = code.strip().split('\n')
        out = ["import * as fs from 'fs';","const inputData = fs.readFileSync(0, 'utf8').split('\n');","let __input_idx = 0;","function input(): string { return inputData[__input_idx++] || ''; }",""]
        for raw in lines:
            s = raw.strip()
            if not s:
                out.append("")
                continue
            m_print = re.match(r'^print\s*\((.*)\)\s*$', s)
            if m_print:
                out.append(f'console.log({m_print.group(1)});')
                continue
            m_int_in = re.match(r'^(\w+)\s*=\s*int\s*\(\s*input\s*\(\s*\)\s*\)\s*$', s)
            if m_int_in:
                var = m_int_in.group(1)
                out.append(f'let {var}: number = parseInt(input());')
                continue
            m_in = re.match(r'^(\w+)\s*=\s*input\s*\(\s*\)\s*$', s)
            if m_in:
                var = m_in.group(1)
                out.append(f'let {var}: string = input();')
                continue
            m_for = re.match(r'^for\s+(\w+)\s+in\s+range\s*\(\s*(\d+)\s*\)\s*:$', s)
            if m_for:
                v, lim = m_for.groups()
                out.append(f'for (let {v} = 0; {v} < {lim}; {v}++) {{')
                continue
            if s.endswith(':'):
                hdr = s[:-1]
                if hdr.startswith('if '):
                    cond = hdr[3:]
                    out.append(f'if ({cond}) {{')
                    continue
            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', s)
            if m_assign:
                var, val = m_assign.groups()
                out.append(f'let {var} = {val};')
                continue
            out.append(f'// {s}')
        return '\n'.join(out)

    def cpp_to_python(self, code):
        result = []
        for line in code.strip().split('\n'):
            s = line.strip()
            # skip empty lines, preprocessor/comments and typical main/brace/return markers
            if not s or s.startswith('#') or 'main()' in s or s in ['{', '}', 'return 0;']:
                continue

            # handle simple cout << ... [<< endl];
            if 'cout <<' in s:
                m = re.search(r'cout\s*<<\s*(.+?)(?:\s*<<\s*endl)?\s*;', s)
                if m:
                    content = m.group(1).strip()
                    # convert C++ stream concatenation into Python + concatenation
                    content = re.sub(r'\s*<<\s*', ' + ', content)
                    result.append(f'print({content})')
                    continue

            # fallback: keep the stripped line for further processing downstream
            result.append(s)

        intermediate = "\n".join(result)
        return self._corregir_cpp_a_python(intermediate)
        return self.python_to_ruby(py)
    def cpp_to_go(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_go(py)
    def cpp_to_rust(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_rust(py)
    def cpp_to_php(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_php(py)
    def cpp_to_typescript(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_typescript(py)
    # Delegaciones faltantes: usar C++ -> Python -> objetivo
    def cpp_to_csharp(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_csharp(py)

    def cpp_to_java(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_java(py)

    def cpp_to_javascript(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_javascript(py)

    def cpp_to_ruby(self, code):
        py = self.cpp_to_python(code)
        return self.python_to_ruby(py)

    def csharp_to_python(self, code):
        lines = code.splitlines()
        result_lines = []
        indent_level = 0
        indent_unit = "    "

        def emit(line):
            result_lines.append(indent_unit * indent_level + line)

        def to_f_string(s):
            # Interpolated strings $"..." -> f"..."
            s = s.replace('$"', 'f"').replace("$'", "f'")
            return s

        def convert_for(header):
            m = re.match(
                r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*([\-\w\.\+]+)\s*;\s*\1\s*(<=|<)\s*([\-\w\.\+]+)\s*;\s*(\1\+\+|\+\+\1|\1\+\+=\s*1)\s*\)\s*',
                header
            )
            if m:
                var, start, op, end, _ = m.groups()
                if op == '<=':
                    if re.match(r'^\-?\d+$', end):
                        end_expr = str(int(end) + 1)
                    else:
                        end_expr = f"({end}) + 1"
                else:
                    end_expr = end
                return f"for {var} in range({start}, {end_expr}):"
            m2 = re.match(r'foreach\s*\(\s*(?:var|[\w<>]+)\s+(\w+)\s+in\s+([^\)]+)\)\s*', header)
            if m2:
                var, coll = m2.groups()
                return f"for {var} in {coll.strip()}:"
            inner = re.sub(r'^\s*for\s*\(', 'for ', header).rstrip()
            inner = re.sub(r'\)\s*$', '', inner)
            return inner + ':'

        for raw in lines:
            s_orig = raw.rstrip('\n')
            s = s_orig.strip()

            # Saltar líneas vacías (pero conservar como separador)
            if not s:
                # evitar acumular muchos blanks al inicio
                if result_lines:
                    result_lines.append("")
                continue

            # Remover atributos C# [Attr]
            s = re.sub(r'^\[.*?\]\s*', '', s).strip()
            if not s:
                continue

            # Manejar "} else {" en una sola línea
            if re.match(r'^\}\s*else\s*\{', s):
                indent_level = max(0, indent_level - 1)
                emit("else:")
                indent_level += 1
                continue

            # Cierre de bloque '}' -> dedent y procesar resto si lo hay
            if s == '}' or s.startswith('}'):
                indent_level = max(0, indent_level - 1)
                remainder = s.lstrip('}').strip()
                if not remainder:
                    continue
                s = remainder

            # Apertura de bloque con '{' al final
            if s.endswith('{'):
                header = s[:-1].strip()
                header = re.sub(r'^(public|private|protected|internal|static|sealed|virtual|override|abstract)\s+', '', header)
                header = to_f_string(header)

                # Omitir firma Main() SIN cambiar indent_level (evita unexpected indent)
                if re.match(r'^(static\s+)?void\s+Main\s*\(', header):
                    # Si quieres envolver en if __name__ descomenta estas dos líneas:
                    # emit('if __name__ == "__main__":')
                    # indent_level += 1
                    continue

                # No incrementar indent para class/namespace: omitimos la cabecera y no cambiamos indent.
                if header.startswith('class ') or header.startswith('namespace '):
                    # simplemente saltamos la cabecera; las llaves serán manejadas por '}'.
                    continue

                # for / if / while / foreach / switch / else if
                if header.startswith('for '):
                    py_header = convert_for(header)
                    emit(py_header)
                    indent_level += 1
                    continue

                if header.startswith('if ') or header.startswith('else if') or header.startswith('else') or header.startswith('while ') or header.startswith('switch '):
                    h = header
                    h = re.sub(r'^else\s+if\s*\(', 'elif (', h)
                    m_cond = re.match(r'^(?:if|elif|while)\s*\((.*)\)\s*$', h)
                    if m_cond:
                        cond = m_cond.group(1).strip()
                        kw = h.split()[0] if h.split() else 'if'
                        emit(f"{kw} {cond}:".replace('if (', 'if ').replace('elif (', 'elif '))
                    else:
                        emit(h + ':')
                    indent_level += 1
                    continue

                # default: emitir header + ":" y entrar en bloque
                emit(header + ':')
                indent_level += 1
                continue

            # Remover ; final y modifiers
            s = s.rstrip(';').strip()
            s = re.sub(r'^(public|private|protected|internal|static|sealed|virtual|override|abstract)\s+', '', s)

            # Interpolated strings
            s = to_f_string(s)

            # Lectura y escritura de consola
            s = re.sub(r'Console\.ReadLine\s*\(\s*\)', r'input()', s)
            s = re.sub(r'Console\.Read\s*\(\s*\)', r'input()[0]', s)
            s = re.sub(r'Console\.WriteLine\s*\(\s*([^\)]*?)\s*\)\s*', r'print(\1)', s)
            s = re.sub(r'Console\.Write\s*\(\s*([^\)]*?)\s*\)\s*', r'print(\1, end="")', s)

            # Parses numéricos
            s = re.sub(r'int\.Parse\s*\(\s*([^\)]+)\s*\)', r'int(\1)', s)
            s = re.sub(r'double\.Parse\s*\(\s*([^\)]+)\s*\)', r'float(\1)', s)
            s = re.sub(r'float\.Parse\s*\(\s*([^\)]+)\s*\)', r'float(\1)', s)

            # Declaraciones con inicialización
            m_decl = re.match(r'^(?:string|int|double|float|bool|char|var)\s+(\w+)\s*(?:=\s*(.+))$', s)
            if m_decl:
                var = m_decl.group(1)
                init = m_decl.group(2).strip()
                emit(f'{var} = {init}')
                continue

            # var keyword
            m_var = re.match(r'^var\s+(\w+)\s*=\s*(.+)$', s)
            if m_var:
                emit(f"{m_var.group(1)} = {m_var.group(2)}")
                continue

            # for(...) sin llaves
            if s.startswith('for ') or s.startswith('for('):
                py_header = convert_for(s)
                emit(py_header)
                continue

            # if/else/while sin llaves
            m_if = re.match(r'^(else\s+if|if|else|while)\s*(?:\((.*)\))?$', s)
            if m_if:
                kw = m_if.group(1)
                cond = m_if.group(2) or ''
                if kw == 'else if':
                    kw_py = 'elif'
                else:
                    kw_py = kw
                if cond:
                    emit(f"{kw_py} {cond}:")
                else:
                    emit(f"{kw_py}:")
                continue

            # Omitir 'using', 'namespace', 'class' sueltos
            if s.startswith('using ') or s.startswith('namespace ') or s.startswith('class '):
                continue

            # Emitir restante
            emit(s)

        # Quitar posibles blanks al inicio/fin
        while result_lines and result_lines[0].strip() == "":
            result_lines.pop(0)
        while result_lines and result_lines[-1].strip() == "":
            result_lines.pop()

        return "\n".join(result_lines)
    def csharp_to_cpp(self, code):
        py = self.csharp_to_python(code)
        return self.python_to_cpp(py)
    def csharp_to_java(self, code):
        return code.replace('Console.WriteLine', 'System.out.println')
    def csharp_to_javascript(self, code):
        return code.replace('Console.WriteLine', 'console.log')
    def csharp_to_ruby(self, code):
        return code.replace('Console.WriteLine', 'puts')
    def csharp_to_go(self, code):
        return code.replace('Console.WriteLine', 'fmt.Println')
    def csharp_to_rust(self, code):
        return code.replace('Console.WriteLine', 'println!')
    def csharp_to_php(self, code):
        return code.replace('Console.WriteLine', 'echo')
    def csharp_to_typescript(self, code):
        return code.replace('Console.WriteLine', 'console.log')

    def java_to_python(self, code):
        lines = code.splitlines()
        out_lines = []
        indent_level = 0
        indent_unit = "    "
        declared_vars = {}
        pending_prompt = None  # Para combinar System.out.print con scanner.nextLine/nextInt
        
        def push_line(text):
            out_lines.append(indent_unit * indent_level + text)
        
        i = 0
        while i < len(lines):
            raw = lines[i]
            orig = raw
            l = raw.strip()
            
            # Verificar si la siguiente línea es scanner.nextLine() o scanner.nextInt()
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            
            if not l:
                push_line("")
                i += 1
                continue
            
            # Comentarios
            if l.startswith('//'):
                push_line(f'# {l[2:].strip()}')
                i += 1
                continue
            
            # Omitir imports, class, main, Scanner declarations
            if any(tok in l for tok in ['import ', 'public class', 'public static void main', 'Scanner scanner']):
                i += 1
                continue
            
            # Omitir scanner.close()
            if 'scanner.close()' in l.lower():
                i += 1
                continue
            
            # Omitir scanner.nextLine() que consume newline (sin asignación)
            if re.match(r'^\s*scanner\.nextLine\s*\(\s*\)\s*;?\s*(//.*)?$', l):
                i += 1
                continue
            
            # Manejar cierre de bloques
            leading_closing = False
            if l.startswith('}'):
                leading_closing = True
                l = l[1:].strip()
                indent_level = max(indent_level - 1, 0)
                if not l:
                    i += 1
                    continue
            
            # Detectar apertura de bloque
            opens_block = False
            if l.endswith('{'):
                opens_block = True
                l = l[:-1].strip()
            
            # System.out.println(...) -> print(...)
            m_print = re.match(r'System\.out\.println\s*\(\s*(.*?)\s*\)\s*;?$', l)
            if m_print:
                arg = m_print.group(1).strip()
                # Convertir concatenación de strings Java a f-string de Python
                if '+' in arg:
                    # Dividir respetando paréntesis
                    parts = []
                    current = ""
                    paren_depth = 0
                    for char in arg:
                        if char == '(':
                            paren_depth += 1
                            current += char
                        elif char == ')':
                            paren_depth -= 1
                            current += char
                        elif char == '+' and paren_depth == 0:
                            parts.append(current.strip())
                            current = ""
                        else:
                            current += char
                    if current:
                        parts.append(current.strip())
                    
                    fparts = []
                    has_expr = False
                    for p in parts:
                        p = p.strip()
                        if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                            txt = p[1:-1].replace('"', '\\"')
                            fparts.append(txt)
                        else:
                            has_expr = True
                            # Remover paréntesis externos si existen
                            p_clean = p
                            if p_clean.startswith('(') and p_clean.endswith(')'):
                                # Verificar que los paréntesis coincidan
                                if p_clean.count('(') == p_clean.count(')'):
                                    p_clean = p_clean[1:-1].strip()
                            fparts.append('{' + p_clean + '}')
                    if has_expr:
                        fcontent = ''.join(fparts)
                        fcontent = fcontent.replace('"', '\\"')
                        push_line(f'print(f"{fcontent}")')
                    else:
                        text = ''.join(fparts)
                        push_line(f'print("{text}")')
                else:
                    push_line(f'print({arg})')
                if opens_block:
                    indent_level += 1
                i += 1
                continue
            
            # System.out.print(...) - verificar si la siguiente línea es scanner
            m_print_no_nl = re.match(r'System\.out\.print\s*\(\s*(.*?)\s*\)\s*;?$', l)
            if m_print_no_nl:
                arg = m_print_no_nl.group(1).strip()
                # Extraer el prompt si es un string literal
                prompt = None
                if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                    prompt = arg[1:-1]
                
                # Verificar si la siguiente línea es scanner.nextLine() o scanner.nextInt()
                # Manejar tanto "String nombre = scanner.nextLine()" como "nombre = scanner.nextLine()"
                # También manejar indentación
                m_next_line = re.search(r'(?:String\s+)?(\w+)\s*=\s*scanner\.nextLine\s*\(\s*\)\s*;?', next_line)
                m_next_int = re.search(r'(?:int\s+)?(\w+)\s*=\s*scanner\.nextInt\s*\(\s*\)\s*;?', next_line)
                
                if m_next_line:
                    var = m_next_line.group(1)
                    if prompt:
                        # Usar input() con prompt directamente para que aparezca en consola pero no en resultado
                        push_line(f'{var} = input("{prompt}")')
                    else:
                        push_line(f'{var} = input()')
                    declared_vars[var] = 'String'
                    i += 2  # Saltar ambas líneas
                    if opens_block:
                        indent_level += 1
                    continue
                elif m_next_int:
                    var = m_next_int.group(1)
                    if prompt:
                        # Usar input() con prompt directamente para que aparezca en consola pero no en resultado
                        push_line(f'{var} = int(input("{prompt}"))')
                    else:
                        push_line(f'{var} = int(input())')
                    declared_vars[var] = 'int'
                    i += 2  # Saltar ambas líneas
                    if opens_block:
                        indent_level += 1
                    continue
                else:
                    # No hay scanner después, solo es un print normal
                    push_line(f'print({arg}, end="")')
                    if opens_block:
                        indent_level += 1
                    i += 1
                    continue
            
            # Scanner.nextLine() -> input() (sin prompt previo)
            # Manejar tanto "String nombre = scanner.nextLine()" como "nombre = scanner.nextLine()"
            m_next_line = re.match(r'(?:String\s+)?(\w+)\s*=\s*scanner\.nextLine\s*\(\s*\)\s*;?$', l)
            if m_next_line:
                var = m_next_line.group(1)
                push_line(f'{var} = input()')
                declared_vars[var] = 'String'
                if opens_block:
                    indent_level += 1
                i += 1
                continue
            
            # Scanner.nextInt() -> int(input()) (sin prompt previo)
            # Manejar tanto "int edad = scanner.nextInt()" como "edad = scanner.nextInt()"
            m_next_int = re.match(r'(?:int\s+)?(\w+)\s*=\s*scanner\.nextInt\s*\(\s*\)\s*;?$', l)
            if m_next_int:
                var = m_next_int.group(1)
                push_line(f'{var} = int(input())')
                declared_vars[var] = 'int'
                if opens_block:
                    indent_level += 1
                i += 1
                continue
            
            # Remover punto y coma
            if l.endswith(';'):
                l = l[:-1].rstrip()
            
            # Declaraciones de variables: String nombre = ... -> nombre = ...
            m_decl_string = re.match(r'String\s+(\w+)\s*=\s*(.+)$', l)
            if m_decl_string:
                var, val = m_decl_string.groups()
                declared_vars[var] = 'String'
                push_line(f'{var} = {val}')
                if opens_block:
                    indent_level += 1
                i += 1
                continue
            
            # Declaraciones int: int edad = ... -> edad = ...
            m_decl_int = re.match(r'int\s+(\w+)\s*=\s*(.+)$', l)
            if m_decl_int:
                var, val = m_decl_int.groups()
                declared_vars[var] = 'int'
                push_line(f'{var} = {val}')
                if opens_block:
                    indent_level += 1
                i += 1
                continue
            
            # Declaraciones double/float
            m_decl_double = re.match(r'(double|float)\s+(\w+)\s*=\s*(.+)$', l)
            if m_decl_double:
                var = m_decl_double.group(2)
                val = m_decl_double.group(3)
                declared_vars[var] = 'double'
                push_line(f'{var} = {val}')
                if opens_block:
                    indent_level += 1
                i += 1
                continue
            
            # if (condición) { -> if condición:
            m_if = re.match(r'if\s*\(\s*(.*?)\s*\)\s*$', l)
            if m_if:
                cond = m_if.group(1).strip()
                push_line(f'if {cond}:')
                indent_level += 1
                i += 1
                continue
            
            # else if (condición) { -> elif condición:
            m_elif = re.match(r'else\s+if\s*\(\s*(.*?)\s*\)\s*$', l)
            if m_elif:
                cond = m_elif.group(1).strip()
                indent_level = max(indent_level - 1, 0)
                push_line(f'elif {cond}:')
                indent_level += 1
                i += 1
                continue
            
            # else { -> else:
            if l.strip() == 'else':
                indent_level = max(indent_level - 1, 0)
                push_line('else:')
                indent_level += 1
                i += 1
                continue
            
            # while (condición) { -> while condición:
            m_while = re.match(r'while\s*\(\s*(.*?)\s*\)\s*$', l)
            if m_while:
                cond = m_while.group(1).strip()
                push_line(f'while {cond}:')
                indent_level += 1
                i += 1
                continue
            
            # for (int i = 0; i < 3; i++) { -> for i in range(3):
            m_for = re.match(r'for\s*\(\s*int\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\+\+\s*\)\s*$', l)
            if m_for:
                var, start, end = m_for.groups()
                if start == '0':
                    push_line(f'for {var} in range({end}):')
                else:
                    push_line(f'for {var} in range({start}, {end}):')
                indent_level += 1
                i += 1
                continue
            
            # Asignaciones simples: variable = valor
            m_assign = re.match(r'^(\w+)\s*=\s*(.+)$', l)
            if m_assign:
                var, val = m_assign.groups()
                push_line(f'{var} = {val}')
                if opens_block:
                    indent_level += 1
                i += 1
                continue
            
            # Línea no reconocida como comentario
            push_line(f'# {l}')
            if opens_block:
                indent_level += 1
            i += 1
        
        # Limpiar líneas vacías al final
        while out_lines and out_lines[-1].strip() == "":
            out_lines.pop()
        
        return '\n'.join(out_lines)
    def java_to_cpp(self, code):
        py = self.java_to_python(code)
        return self.python_to_cpp(py)
    def java_to_csharp(self, code):
        return code.replace('System.out.println', 'Console.WriteLine')
    def java_to_javascript(self, code):
        return code.replace('System.out.println', 'console.log')
    def java_to_ruby(self, code):
        return code.replace('System.out.println', 'puts')
    def java_to_go(self, code):
        return code.replace('System.out.println', 'fmt.Println')
    def java_to_rust(self, code):
        return code.replace('System.out.println', 'println!')
    def java_to_php(self, code):
        return code.replace('System.out.println', 'echo')
    def java_to_typescript(self, code):
        return code.replace('System.out.println', 'console.log')

    def javascript_to_python(self, code):
        return code.replace('console.log', 'print')
    def javascript_to_cpp(self, code):
        py = self.javascript_to_python(code)
        return self.python_to_cpp(py)
    def javascript_to_csharp(self, code):
        return code.replace('console.log', 'Console.WriteLine')
    def javascript_to_java(self, code):
        return code.replace('console.log', 'System.out.println')
    def javascript_to_ruby(self, code):
        return code.replace('console.log', 'puts')
    def javascript_to_go(self, code):
        return code.replace('console.log', 'fmt.Println')
    def javascript_to_rust(self, code):
        return code.replace('console.log', 'println!')
    def javascript_to_php(self, code):
        return code.replace('console.log', 'echo')
    def javascript_to_typescript(self, code):
        return code

    def ruby_to_python(self, code):
        return code.replace('puts', 'print')
    def ruby_to_cpp(self, code):
        py = self.ruby_to_python(code)
        return self.python_to_cpp(py)
    def ruby_to_csharp(self, code):
        return code.replace('puts', 'Console.WriteLine')
    def ruby_to_java(self, code):
        return code.replace('puts', 'System.out.println')
    def ruby_to_javascript(self, code):
        return code.replace('puts', 'console.log')
    def ruby_to_go(self, code):
        return code.replace('puts', 'fmt.Println')
    def ruby_to_rust(self, code):
        return code.replace('puts', 'println!')
    def ruby_to_php(self, code):
        return code.replace('puts', 'echo')
    def ruby_to_typescript(self, code):
        return code.replace('puts', 'console.log')

    def go_to_python(self, code):
        return code.replace('fmt.Println', 'print')
    def go_to_cpp(self, code):
        py = self.go_to_python(code)
        return self.python_to_cpp(py)
    def go_to_csharp(self, code):
        return code.replace('fmt.Println', 'Console.WriteLine')
    def go_to_java(self, code):
        return code.replace('fmt.Println', 'System.out.println')
    def go_to_javascript(self, code):
        return code.replace('fmt.Println', 'console.log')
    def go_to_ruby(self, code):
        return code.replace('fmt.Println', 'puts')
    def go_to_rust(self, code):
        return code.replace('fmt.Println', 'println!')
    def go_to_php(self, code):
        return code.replace('fmt.Println', 'echo')
    def go_to_typescript(self, code):
        return code.replace('fmt.Println', 'console.log')

    def rust_to_python(self, code):
        return code.replace('println!', 'print')
    def rust_to_cpp(self, code):
        py = self.rust_to_python(code)
        return self.python_to_cpp(py)
    def rust_to_csharp(self, code):
        return code.replace('println!', 'Console.WriteLine')
    def rust_to_java(self, code):
        return code.replace('println!', 'System.out.println')
    def rust_to_javascript(self, code):
        return code.replace('println!', 'console.log')
    def rust_to_ruby(self, code):
        return code.replace('println!', 'puts')
    def rust_to_go(self, code):
        return code.replace('println!', 'fmt.Println')
    def rust_to_php(self, code):
        return code.replace('println!', 'echo')
    def rust_to_typescript(self, code):
        return code.replace('println!', 'console.log')

    def php_to_python(self, code):
        return code.replace('echo', 'print')
    def php_to_cpp(self, code):
        py = self.php_to_python(code)
        return self.python_to_cpp(py)
    def php_to_csharp(self, code):
        return code.replace('echo', 'Console.WriteLine')
    def php_to_java(self, code):
        return code.replace('echo', 'System.out.println')
    def php_to_javascript(self, code):
        return code.replace('echo', 'console.log')
    def php_to_ruby(self, code):
        return code.replace('echo', 'puts')
    def php_to_go(self, code):
        return code.replace('echo', 'fmt.Println')
    def php_to_rust(self, code):
        return code.replace('echo', 'println!')
    def php_to_typescript(self, code):
        return code.replace('echo', 'console.log')

    def typescript_to_python(self, code):
        return code.replace('console.log', 'print')
    def typescript_to_cpp(self, code):
        py = self.typescript_to_python(code)
        return self.python_to_cpp(py)
    def typescript_to_csharp(self, code):
        return code.replace('console.log', 'Console.WriteLine')
    def typescript_to_java(self, code):
        return code.replace('console.log', 'System.out.println')
    def typescript_to_javascript(self, code):
        return code
    def typescript_to_ruby(self, code):
        return code.replace('console.log', 'puts')
    def typescript_to_go(self, code):
        return code.replace('console.log', 'fmt.Println')
    def typescript_to_rust(self, code):
        return code.replace('console.log', 'println!')
    def typescript_to_php(self, code):
        return code.replace('console.log', 'echo')

    def _corregir_cpp_a_python(self, codigo_cpp: str) -> str:
        lines = codigo_cpp.splitlines()
        out_lines = []
        indent_level = 0
        types = {}
        indent_unit = "    "

        def push_line(text):
            out_lines.append(indent_unit * indent_level + text)

        for raw in lines:
            orig = raw
            l = raw.strip()
            if not l:
                push_line("")
                continue

            if l.startswith('//'):
                push_line(f'# {l[2:].strip()}')
                continue

            if any(tok in l for tok in ['#include', 'using namespace', 'int main', 'return 0']):
                continue

            if re.match(r'cin\s*\.?ignore\s*$$.*$$\s*;?$', l) or re.match(r'cin\s*\.?ignore\s*\(\s*\)\s*;?$', l):
                continue

            leading_closing = False
            if l.startswith('}'):
                leading_closing = True
                l = l[1:].strip()
                indent_level = max(indent_level - 1, 0)
                if not l:
                    continue

            opens_block = False
            if l.endswith('{'):
                opens_block = True
                l = l[:-1].strip()

            m = re.match(r'getline\s*$$\s*cin\s*,\s*(.+?)\s*$$\s*;?$', l)
            if not m:
                m = re.match(r'getline\s*\(\s*cin\s*,\s*(\w+)\s*\)\s*;?$', l)
            if m:
                var = m.group(1).strip()
                push_line(f'{var} = input()')
                if opens_block:
                    indent_level += 1
                continue

            m = re.match(r'cin\s*>>\s*(\w+)\s*;?$', l)
            if m:
                var = m.group(1)
                vartype = types.get(var)
                if vartype == 'int':
                    push_line(f'{var} = int(input())')
                elif vartype in ('double', 'float'):
                    push_line(f'{var} = float(input())')
                else:
                    push_line(f'{var} = input()')
                if opens_block:
                    indent_level += 1
                continue

            if 'stoi(' in l:
                l = re.sub(r'stoi\s*\(\s*(.*?)\s*\)', r'int(\1)', l)

            if l.endswith(';'):
                l = l[:-1].rstrip()

            m_decl = re.match(r'^(string|int|double|float|bool)\s+(\w+)(\s*=\s*(.*))?$', l)
            if m_decl:
                typ = m_decl.group(1)
                var = m_decl.group(2)
                init = m_decl.group(4)
                types[var] = typ
                if init:
                    val = init.strip()
                    if typ == 'int' and re.match(r'^\d+$', val):
                        push_line(f'{var} = {val}')
                    elif typ in ('double', 'float') and re.match(r'^\d+(\.\d+)?$', val):
                        push_line(f'{var} = {val}')
                    else:
                        push_line(f'{var} = {val}')
                if opens_block:
                    indent_level += 1
                continue

            if l.startswith('print(') and l.endswith(')'):
                inner = l[6:-1].strip()
                parts = [p.strip() for p in re.split(r'\s*\+\s*', inner)]
                has_expr = False
                fparts = []
                for p in parts:
                    if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
                        # literal text
                        txt = p[1:-1].replace('"', '\\"')
                        fparts.append(txt)
                    else:
                        has_expr = True
                        # remove redundant str(...) wrapper
                        mstr = re.match(r'^str\((.*)\)$', p)
                        expr = mstr.group(1) if mstr else p
                        fparts.append('{' + expr + '}')

                if has_expr:
                    fcontent = ''.join(fparts)
                    # escape any double quotes inside
                    fcontent = fcontent.replace('"', '\\"')
                    push_line(f'print(f"{fcontent}")')
                else:
                    # only literals
                    text = ''.join(fparts)
                    push_line(f'print("{text}")')

                if opens_block:
                    indent_level += 1
                continue

            m_if = re.match(r'^if\s*$$(.*?)$$\s*$', l)
            if m_if:
                cond = m_if.group(1).strip()
                push_line(f'if {cond}:')
                indent_level += 1
                continue

            m_elif = re.match(r'^else\s+if\s*$$(.*?)$$\s*$', l)
            if m_elif:
                cond = m_elif.group(1).strip()
                if not leading_closing:
                    indent_level = max(indent_level - 1, 0)
                push_line(f'elif {cond}:')
                indent_level += 1
                continue

            m_else = re.match(r'^else\s*$', l)
            if m_else:
                if not leading_closing:
                    indent_level = max(indent_level - 1, 0)
                push_line('else:')
                indent_level += 1
                continue

            m_for = re.match(r'for\s*$$\s*int\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\+\+\s*$$\s*$', l)
            if not m_for:
                m_for = re.match(r'for\s*\(\s*int\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\+\+\s*\)\s*$', l)
            if m_for:
                var, start, end = m_for.groups()
                if start == '0':
                    push_line(f'for {var} in range({end}):')
                else:
                    push_line(f'for {var} in range({start}, {end}):')
                indent_level += 1
                continue

            m_while = re.match(r'while\s*$$(.*)$$\s*$', l)
            if m_while:
                cond = m_while.group(1).strip()
                push_line(f'while {cond}:')
                indent_level += 1
                continue

            if re.match(r'\w+\s*=\s*.*', l):
                push_line(l)
                if opens_block:
                    indent_level += 1
                continue

            # Manejar estructuras comunes con paréntesis que no fueron capturadas antes
            m_plain_if = re.match(r'^(else\s+if|if)\s*\((.*)\)\s*;?$', l)
            if m_plain_if:
                kw = m_plain_if.group(1)
                cond = m_plain_if.group(2).strip()
                if kw == 'else if':
                    # ajustar dedent si la llave de cierre no fue leída
                    push_line(f'elif {cond}:')
                else:
                    push_line(f'if {cond}:')
                indent_level += 1
                continue

            m_plain_else = re.match(r'^else\s*;?$', l)
            if m_plain_else:
                push_line('else:')
                indent_level += 1
                continue

            m_plain_while = re.match(r'^while\s*\((.*)\)\s*;?$', l)
            if m_plain_while:
                cond = m_plain_while.group(1).strip()
                push_line(f'while {cond}:')
                indent_level += 1
                continue

            if '//' in orig:
                comment = orig.split('//', 1)[1].strip()
                push_line(f'# {comment}')
                continue

            # Heurísticas básicas para línea no manejada: intentar una conversión simple
            s = l
            # booleanos
            s = re.sub(r'\btrue\b', 'True', s)
            s = re.sub(r'\bfalse\b', 'False', s)
            # operadores lógicos
            s = s.replace('&&', ' and ').replace('||', ' or ')
            # negación (simple) - evitar reemplazos dentro de tokens (aprox.)
            s = re.sub(r'\!\s*', ' not ', s)
            # eliminar calificadores de std::
            s = re.sub(r'std::', '', s)
            # punteros/miembros -> convertir -> a .
            s = s.replace('->', '.')
            # quitar punto y coma final si existe
            if s.endswith(';'):
                s = s[:-1].rstrip()

            # Si la línea parece una asignación o llamada, emítela; si no, emitir como comentario claro
            if re.match(r'^[\w\[\]\.(\)\"\'"\s\,\+\-\*/%]+$', s) or '=' in s or s.endswith(')'):
                push_line(s)
            else:
                push_line(f'# NO_TRADUCIDO (aprox): {s}')
            if opens_block:
                indent_level += 1

        return "\n".join(out_lines)

def run_translated_code(code: str, lang_key: str, stdin_data: str = "", timeout: int = 10):
    tmpdir = tempfile.mkdtemp(prefix="ctrans_")
    try:
        expects = 0
        if lang_key == "python":
            expects = len(re.findall(r'\binput\s*\(', code))
        elif lang_key == "cpp":
            expects = len(re.findall(r'\bcin\s*>>', code)) + len(re.findall(r'getline\s*\(\s*cin\s*,', code))
        elif lang_key == "java":
            expects = len(re.findall(r'Scanner|nextLine|nextInt', code))
        elif lang_key == "csharp":
            expects = len(re.findall(r'Console\.ReadLine', code))
        elif lang_key == "ruby":
            expects = len(re.findall(r'gets\.chomp', code))
        elif lang_key == "go":
            expects = len(re.findall(r'fmt\.Scan', code))

        def _auto_fill_stdin(code_text: str, lang: str, count: int) -> str:
            if count <= 0:
                return ""
            lines = []
            if lang == "python":
                pattern = re.compile(r'int\s*\(\s*input\s*\(|input\s*\(')
                for m in pattern.finditer(code_text):
                    token = m.group(0)
                    if token.strip().startswith('int'):
                        lines.append('0')
                    else:
                        lines.append('usuario')
                while len(lines) < count:
                    lines.append('0')
            else:
                lines = ['0'] * count
            return "\n".join(lines)

        if expects > 0 and (stdin_data is None or stdin_data.strip() == ""):
            stdin_data = _auto_fill_stdin(code, lang_key, expects)

        input_bytes = stdin_data.encode() if stdin_data else None

        if lang_key == "python":
            src_path = os.path.join(tmpdir, "prog.py")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            proc = subprocess.run([sys.executable, src_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            output = proc.stdout.decode(errors="replace")
            # Filtrar prompts de input() de la salida
            # Los prompts aparecen como líneas que terminan con ":" y contienen palabras clave comunes
            lines = output.split('\n')
            filtered_lines = []
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                # Detectar si es un prompt común (termina con ":" y contiene palabras clave de entrada)
                is_prompt = (stripped.endswith(':') and 
                            any(keyword in stripped.lower() for keyword in 
                                ['ingresa', 'ingrese', 'introduce', 'introduzca', 'escribe', 'escriba', 
                                 'dame', 'dé', 'nombre', 'edad', 'valor', 'número', 'numero', 'dato']))
                
                # No incluir líneas que son claramente prompts
                if not is_prompt:
                    filtered_lines.append(line)
            
            output = '\n'.join(filtered_lines)
            return proc.returncode == 0, output

        elif lang_key == "cpp":
            if shutil.which("g++") is None:
                return False, "g++ no encontrado. Instala MinGW/MSYS2 y agrega g++ al PATH."
            src_path = os.path.join(tmpdir, "prog.cpp")
            exe_path = os.path.join(tmpdir, "prog.exe" if sys.platform == "win32" else "prog")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            cproc = subprocess.run(["g++", src_path, "-o", exe_path],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            if cproc.returncode != 0:
                return False, f"Error al compilar C++:\n{cproc.stdout.decode(errors='replace')}"
            proc = subprocess.run([exe_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "java":
            if shutil.which("javac") is None or shutil.which("java") is None:
                return False, "Java (javac/java) no encontrado. Asegúrate de que esté instalado y en el PATH."
            src_path = os.path.join(tmpdir, "Main.java")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            cproc = subprocess.run(["javac", "-d", tmpdir, src_path],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            if cproc.returncode != 0:
                return False, f"Error al compilar Java:\n{cproc.stdout.decode(errors='replace')}"
            proc = subprocess.run(["java", "-cp", tmpdir, "Main"], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "csharp":
            if shutil.which("csc") is None:
                return False, "csc no encontrado. Instala .NET SDK y agrega csc al PATH."
            src_path = os.path.join(tmpdir, "prog.cs")
            exe_path = os.path.join(tmpdir, "prog.exe" if sys.platform == "win32" else "prog")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            cproc = subprocess.run(["csc", "/out:" + exe_path, src_path],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            if cproc.returncode != 0:
                return False, f"Error al compilar C#:\n{cproc.stdout.decode(errors='replace')}"
            proc = subprocess.run([exe_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "javascript":
            if shutil.which("node") is None:
                return False, "Node.js no encontrado. Instala Node.js y agrega node al PATH."
            src_path = os.path.join(tmpdir, "prog.js")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            proc = subprocess.run(["node", src_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "ruby":
            if shutil.which("ruby") is None:
                return False, "Ruby no encontrado. Instala Ruby y agrega ruby al PATH."
            src_path = os.path.join(tmpdir, "prog.rb")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            proc = subprocess.run(["ruby", src_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "go":
            if shutil.which("go") is None:
                return False, "Go no encontrado. Instala Go y agrega go al PATH."
            src_path = os.path.join(tmpdir, "prog.go")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            build_proc = subprocess.run(["go", "build", "-o", os.path.join(tmpdir, "prog"), src_path],
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            if build_proc.returncode != 0:
                return False, f"Error al compilar Go:\n{build_proc.stdout.decode(errors='replace')}"
            proc = subprocess.run([os.path.join(tmpdir, "prog")], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "rust":
            if shutil.which("rustc") is None:
                return False, "rustc no encontrado. Instala Rust y agrega rustc al PATH."
            src_path = os.path.join(tmpdir, "prog.rs")
            exe_path = os.path.join(tmpdir, "prog" if sys.platform == "win32" else "prog")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            cproc = subprocess.run(["rustc", src_path, "-o", exe_path],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            if cproc.returncode != 0:
                return False, f"Error al compilar Rust:\n{cproc.stdout.decode(errors='replace')}"
            proc = subprocess.run([exe_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "php":
            if shutil.which("php") is None:
                return False, "PHP no encontrado. Instala PHP y agrega php al PATH."
            src_path = os.path.join(tmpdir, "prog.php")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            proc = subprocess.run(["php", src_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")

        elif lang_key == "typescript":
            if shutil.which("tsc") is None:
                return False, "tsc no encontrado. Instala Node.js y TypeScript (npm install -g typescript) y agrega tsc al PATH."
            js_path = os.path.join(tmpdir, "prog.js")
            src_path = os.path.join(tmpdir, "prog.ts")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)
            compile_proc = subprocess.run(["tsc", src_path, "--outFile", js_path],
                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            if compile_proc.returncode != 0:
                return False, f"Error al compilar TypeScript:\n{compile_proc.stdout.decode(errors='replace')}"
            if shutil.which("node") is None:
                return False, "Node.js no encontrado. Instala Node.js y agrega node al PATH."
            proc = subprocess.run(["node", js_path], input=input_bytes,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0, proc.stdout.decode(errors="replace")


        return False, f"Ejecución no soportada para el lenguaje: {lang_key}"

    except subprocess.TimeoutExpired:
        return False, "Timeout: La ejecución tardó demasiado."
    except Exception as e:
        return False, f"Error al ejecutar: {e}"
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass

def auto_fill_for_ui(code: str, lang_key: str) -> str:
    expects = 0
    if lang_key == "python":
        expects = len(re.findall(r'\binput\s*\(', code))
    elif lang_key == "cpp":
        expects = len(re.findall(r'\bcin\s*>>', code)) + len(re.findall(r'getline\s*\(\s*cin\s*,', code))
    elif lang_key == "java":
        expects = len(re.findall(r'Scanner|nextLine|nextInt', code))
    elif lang_key == "csharp":
        expects = len(re.findall(r'Console\.ReadLine', code))
    elif lang_key == "ruby":
        expects = len(re.findall(r'gets\.chomp', code))
    elif lang_key == "go":
        expects = len(re.findall(r'fmt\.Scan', code))
    
    if expects == 0:
        return ""
    lines = []
    pattern_py = re.compile(r'int\s*\(\s*input\s*\(|input\s*\(')
    if lang_key == "python":
        for m in pattern_py.finditer(code):
            token = m.group(0)
            if token.strip().startswith('int'):
                lines.append('0')
            else:
                lines.append('usuario')
        while len(lines) < expects: # Corrected 'count' to 'expects'
            lines.append('0')
    else:
        lines = ['0'] * expects
    return "\n".join(lines)

def main():
    st.set_page_config(
        page_title="Syntax/Code",
        page_icon="→",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Fira+Code:wght@400;600&display=swap');
       
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 25%, #312e81 50%, #1e293b 75%, #0f172a 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: #f1f5f9;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
       
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
       
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 30%, #312e81 60%, #1e293b 100%);
            padding: 3rem 2.5rem 2rem;
            text-align: center;
            margin: -2rem -2rem 3rem;
            border-radius: 0 0 32px 32px;
            box-shadow: 0 25px 80px rgba(15, 23, 42, 0.4);
            position: relative;
            overflow: hidden;
            animation: heroGlow 3s ease-in-out infinite alternate;
        }
       
        @keyframes heroGlow {
            0% { box-shadow: 0 25px 80px rgba(30, 27, 75, 0.4); }
            100% { box-shadow: 0 25px 80px rgba(49, 46, 129, 0.6); }
        }
       
        .hero-title {
            font-size: 4rem;
            font-weight: 900;
            color: #3B82F6 !important;
            text-shadow: 0 6px 30px rgba(0,0,0,0.4);
            margin-bottom: 0.8rem;
            letter-spacing: -2px;
            animation: titleFloat 3s ease-in-out infinite;
            word-break: break-word;
            white-space: normal;
        }
       
        @keyframes titleFloat {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
       
        .hero-subtitle {
            font-size: 1.4rem;
            color: rgba(241,245,249,0.85);
            font-weight: 600;
            margin-bottom: 2rem;
        }
       
        .hero-badges {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }
       
        .hero-badge {
            background: rgba(59, 130, 246, 0.15);
            backdrop-filter: blur(12px);
            padding: 0.65rem 1.5rem;
            border-radius: 25px;
            font-weight: 700;
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
       
        .hero-badge:hover {
            background: rgba(59, 130, 246, 0.25);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        }

        .lang-selection-container {
            /* Ocultar recuadro: quitar fondo, borde y sombra para que no aparezca */
            background: transparent !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            padding: 0.4rem 0 !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            border: none !important;
            margin: 0 auto 0.6rem !important;
            max-width: 100% !important;
            min-height: 0 !important;
        }

        .lang-selection-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: #e0e7ff;
            text-align: center;
            margin-bottom: 2rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
       
        .lang-container {
            display: flex;
            align-items: center;
            gap: 2rem;
            margin: 0;
        }
       
        .lang-selector {
            display: block;
            background: rgba(10, 14, 20, 0.6);
            backdrop-filter: blur(20px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            border: 2px solid rgba(59, 130, 246, 0.2);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            flex: 1;
        }
       
        .lang-selector:hover {
            border-color: rgba(59, 130, 246, 0.5);
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 50px rgba(59, 130, 246, 0.3);
        }
       
        .lang-label {
            font-weight: 800;
            font-size: 1.1rem;
            color: #e0e7ff;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: center;
        }

        .python-badge {
            background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 20px;
            font-weight: 900;
            font-size: 1.8rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
            border: 3px solid rgba(255, 255, 255, 0.2);
            flex: 1;
        }
       
        .arrow-separator {
            font-size: 3rem;
            color: #3B82F6;
            font-weight: 900;
            animation: arrowPulse 2s ease-in-out infinite;
            text-align: center;
        }
       
        @keyframes arrowPulse {
            0%, 100% { transform: scale(1); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; }
        }
       
        /* Simplified code panel: make it visually minimal so "cuadros" desaparecen */
        .code-panel {
            background: transparent !important;
            backdrop-filter: none !important;
            padding: 0 !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            border: none !important;
            margin-bottom: 0 !important;
            min-height: 0 !important;
            position: static !important;
            overflow: visible !important;
        }

        .code-panel::before {
            display: none !important;
        }
       
        .code-header {
            font-weight: 800;
            font-size: 1.25rem;
            color: #f1f5f9;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(59, 130, 246, 0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
       
        .stTextArea > div > div > textarea {
            background: rgba(10, 14, 20, 0.95) !important;
            color: #f1f5f9 !important;
            border: 2px solid rgba(59, 130, 246, 0.25) !important;
            border-radius: 16px !important;
            font-family: 'Fira Code', monospace !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
            padding: 1.1rem !important;
            resize: vertical !important;
            white-space: pre-wrap !important;
        }
       
        .stTextArea > div > div > textarea:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 6px rgba(59, 130, 246, 0.12) !important;
        }
       
        .stSelectbox > div > div {
            background: rgba(15, 20, 25, 0.95) !important;
            border: 2px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 14px !important;
            color: #f1f5f9 !important;
            font-weight: 700 !important;
            padding: 0.5rem !important;
        }
       
        .stButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #2563eb 50%, #1d4ed8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.9rem 2.5rem !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }

        .stSidebar .stButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 6px 18px rgba(59, 130, 246, 0.25) !important;
            margin-bottom: 0.6rem !important;
            width: 100% !important;
        }

        .stSidebar .stDownloadButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%) !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.4rem !important;
            width: 100% !important;
        }

        /* Hacer que el botón de descarga en el área principal tenga el mismo estilo que los botones primarios */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #2563eb 50%, #1d4ed8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.9rem 2.5rem !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            width: 100% !important;
        }

        .stButton > button:hover {
            transform: translateY(-3px) scale(1.03) !important;
            box-shadow: 0 12px 35px rgba(59, 130, 246, 0.6) !important;
        }
       
        .success-box {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            padding: 1.2rem 1.8rem;
            border-radius: 14px;
            color: white;
            font-weight: 700;
            margin: 1.5rem 0;
            box-shadow: 0 6px 20px rgba(0, 185, 129, 0.4);
            border-left: 5px solid #34d399;
        }
       
        .warning-box {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            padding: 1.2rem 1.8rem;
            border-radius: 14px;
            color: white;
            font-weight: 700;
            margin: 1.5rem 0;
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
            border-left: 5px solid #fbbf24;
        }
       
        .error-box {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            padding: 1.2rem 1.8rem;
            border-radius: 14px;
            color: white;
            font-weight: 700;
            margin: 1.5rem 0;
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
            border-left: 5px solid #f87171;
        }
       
        hr {
            border: none;
            height: 3px;
            background: linear-gradient(90deg, transparent 0%, #3B82F6 20%, #2563eb 50%, #3B82F6 80%, transparent 100%);
            margin: 3rem 0;
            border-radius: 2px;
        }
       
        .history-card {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(10px);
            padding: 1.2rem;
            border-radius: 14px;
            margin-bottom: 1.2rem;
            border-left: 4px solid #3B82F6;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
       
        .history-card:hover {
            transform: translateX(8px);
            box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4);
            border-left-color: #2563eb;
        }
       
        .stat-card {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            border: 2px solid rgba(59, 130, 246, 0.2);
            transition: all 0.3s ease;
        }
       
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
        }
       
        .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #3B82F6, #2563eb, #1d4ed8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
       
        .stat-label {
            font-size: 0.9rem;
            color: #cbd5e1;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('''
        <div class="hero-section">
            <div class="hero-title">Syntax/Code</div>
            <div class="hero-subtitle">Traductor de Código a Python</div>
            <div class="hero-badges">
                <span class="hero-badge">10 Lenguajes</span>
                <span class="hero-badge">Traducción a Python</span>
                <span class="hero-badge">Ejecución Directa</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    translator = CodeTranslator()

    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'code_input' not in st.session_state:
        st.session_state.code_input = ''

    st.markdown('<div class="lang-selection-container">', unsafe_allow_html=True)
    st.markdown('<div class="lang-selection-title">Selecciona el Lenguaje de Origen</div>', unsafe_allow_html=True)
    
    col1, col_arrow, col2 = st.columns([5, 1, 5])
   
    with col1:
        from_lang = st.selectbox(
            "Lenguaje Origen",
            ["C++", "C#", "Java", "JavaScript", "Ruby", "Go", "Rust", "PHP", "TypeScript"],
            key="from_lang",
            label_visibility="collapsed",
            format_func=lambda x: f"{x}"
        )
   
    with col_arrow:
        st.markdown('<div class="arrow-separator">→</div>', unsafe_allow_html=True)
   
    with col2:
        to_lang = st.selectbox(
            "Lenguaje Destino",
            ["Python", "C++", "C#", "Java", "JavaScript", "Ruby", "Go", "Rust", "PHP", "TypeScript"],
            key="to_lang",
            label_visibility="collapsed",
            format_func=lambda x: f"{x}"
        )

    st.markdown('</div>', unsafe_allow_html=True) # Changed from </div class="lang-selection-container"> to </div> to fix the error.

    examples = {
        "Python": '# Ejemplo interactivo\nnombre = input("Ingresa tu nombre: ")\nedad = int(input("Ingresa tu edad: "))\nprint(f"Hola {nombre}, tienes {edad} años.")\n\nif edad >= 18:\n    print("Eres mayor de edad.")\nelse:\n    print("Eres menor de edad.")\n\nfor i in range(3):\n    print(f"Iteración {i + 1}")',
        "C++": '#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    string nombre;\n    int edad;\n    cout << "Ingresa tu nombre: ";\n    getline(cin, nombre);\n    cout << "Ingresa tu edad: ";\n    cin >> edad;\n    cin.ignore();\n    cout << "Hola " << nombre << ", tienes " << edad << " anos." << endl;\n    \n    if (edad >= 18) {\n        cout << "Eres mayor de edad." << endl;\n    } else {\n        cout << "Eres menor de edad." << endl;\n    }\n    \n    for (int i = 0; i < 3; i++) {\n        cout << "Iteraciin " << i + 1 << endl;\n    }\n    \n    return 0;\n}',
        "C#": 'using System;\n\nclass Program {\n    static void Main() {\n        Console.Write("Ingresa tu nombre: ");\n        string nombre = Console.ReadLine();\n        Console.Write("Ingresa tu edad: ");\n        int edad = int.Parse(Console.ReadLine());\n        Console.WriteLine($"Hola {nombre}, tienes {edad} anos.");\n        \n        if (edad >= 18) {\n            Console.WriteLine("Eres mayor de edad.");\n        } else {\n            Console.WriteLine("Eres menor de edad.");\n        }\n        \n        for (int i = 0; i < 3; i++) {\n            Console.WriteLine($"Iteración {i + 1}");\n        }\n    }\n}',
        "Java": 'import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        System.out.print("Ingresa tu nombre: ");\n        String nombre = scanner.nextLine();\n        System.out.print("Ingresa tu edad: ");\n        int edad = scanner.nextInt();\n        scanner.nextLine(); // Consume newline\n        System.out.println("Hola " + nombre + ", tienes " + edad + " anos.");\n\n        if (edad >= 18) {\n            System.out.println("Eres mayor de edad.");\n        } else {\n            System.out.println("Eres menor de edad.");\n        }\n\n        for (int i = 0; i < 3; i++) {\n            System.out.println("" + (i + 1));\n        }\n        scanner.close();\n    }\n}',
        "JavaScript": 'const readline = require("readline").createInterface({\n  input: process.stdin,\n  output: process.stdout,\n});\n\nlet nombre;\nlet edad;\n\nreadline.question("Ingresa tu nombre: ", (name) => {\n  nombre = name;\n  readline.question("Ingresa tu edad: ", (age) => {\n    edad = parseInt(age);\n    console.log(`Hola ${nombre}, tienes ${edad} anos.`);\n\n    if (edad >= 18) {\n      console.log("Eres mayor de edad.");\n    } else {\n      console.log("Eres menor de edad.");\n    }\n\n    for (let i = 0; i < 3; i++) {\n      console.log(`Iteración ${i + 1}`);\n    }\n    readline.close();\n  });\n});',
        "Ruby": 'print "Ingresa tu nombre: "\nnombre = gets.chomp\nprint "Ingresa tu edad: "\nedad = gets.chomp.to_i\n\nputs "Hola #{nombre}, tienes #{edad} años."\n\nif edad >= 18\n  puts "Eres mayor de edad."\nelse\n  puts "Eres menor de edad."\nend\n\nfor i in 1..3\n  puts "Iteración #{i}"\nend',
        "Go": 'package main\n\nimport (\n    "fmt"\n    "bufio"\n    "os"\n    "strconv"\n    "strings"\n)\n\nfunc main() {\n    reader := bufio.NewReader(os.Stdin)\n\n    fmt.Print("Ingresa tu nombre: ")\n    nombre, _ := reader.ReadString(\'\\n\')\n    nombre = strings.TrimSpace(nombre)\n\n    fmt.Print("Ingresa tu edad: ")\n    edadStr, _ := reader.ReadString(\'\\n\')\n    edad, _ := strconv.Atoi(strings.TrimSpace(edadStr))\n\n    fmt.Printf("Hola %s, tienes %d anos.\\n", nombre, edad)\n\n    if edad >= 18 {\n        fmt.Println("Eres mayor de edad.")\n    } else {\n        fmt.Println("Eres menor de edad.")\n    }\n\n    for i := 1; i <= 3; i++ {\n        fmt.Printf(" %d\\n", i)\n    }\n}',
        "Rust": 'use std::io;\n\nfn main() {\n    println!("Ingresa tu nombre: ");\n    let mut nombre = String::new();\n    io::stdin().read_line(&mut nombre).expect("Failed to read line");\n    let nombre = nombre.trim();\n\n    println!("Ingresa tu edad: ");\n    let mut edad_str = String::new();\n    io::stdin().read_line(&mut edad_str).expect("Failed to read line");\n    let edad: i32 = edad_str.trim().parse().expect("Please type a number!");\n\n    println!("Hola {}, tienes {} anos.", nombre, edad);\n\n    if edad >= 18 {\n        println!("Eres mayor de edad.");\n    } else {\n        println!("Eres menor de edad.");\n    }\n\n    for i in 1..=3 {\n        println!(" {}", i);\n    }\n}',
        "PHP": '<?php\necho "Ingresa tu nombre: ";\n$nombre = trim(fgets(STDIN));\necho "Ingresa tu edad: ";\n$edad = (int)trim(fgets(STDIN));\n\necho "Hola " . $nombre . ", tienes " . $edad . " anos.\\n";\n\nif ($edad >= 18) {\n    echo "Eres mayor de edad.\\n";\n} else {\n    echo "Eres menor de edad.\\n";\n}\n\nfor ($i = 1; $i <= 3; $i++) {\n    echo "Iteración " . $i . "\\n";\n}\n?>',
        "TypeScript": 'import * as readline from "readline";\n\nconst rl = readline.createInterface({\n  input: process.stdin,\n  output: process.stdout,\n});\n\nlet nombre: string;\nlet edad: number;\n\nrl.question("Ingresa tu nombre: ", (name) => {\n  nombre = name;\n  rl.question("Ingresa tu edad: ", (age) => {\n    edad = parseInt(age);\n    console.log(`Hola ${nombre}, tienes ${edad} anos.`);\n\n    if (edad >= 18) {\n      console.log("Eres mayor de edad.");\n    } else {\n      console.log("Eres menor de edad.");\n    }\n\n    for (let i = 0; i < 3; i++) {\n      console.log(`Iteración ${i + 1}`);\n    }\n    rl.close();\n  });\n});'
    }

    tabs = st.tabs(["Entrada", "Salida"])
    tab_input, tab_output = tabs

    with tab_input:
        st.markdown('<div class="code-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="code-header">Código de Entrada - {from_lang}</div>', unsafe_allow_html=True)

        col_ex1, col_ex2 = st.columns([1, 1])
        with col_ex1:
            if st.button("Cargar Ejemplo", key="load_example", use_container_width=True):
                st.session_state.code_input = examples.get(from_lang, "")
                st.rerun()
        with col_ex2:
            if st.button("Limpiar", key="clear_input", use_container_width=True):
                st.session_state.code_input = ""
                st.rerun()

        code_input = st.text_area(
            "",
            value=st.session_state.get('code_input', examples.get(from_lang, "")),
            height=400,
            key="code_input",
            label_visibility="collapsed",
            placeholder=f"Escribe o pega tu código en {from_lang} aquí..."
        )

        if code_input.strip():
            lines = len(code_input.split('\n'))
            chars = len(code_input)
            st.markdown(f"<small>{lines} líneas | {chars} caracteres</small>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab_output:
        st.markdown('<div class="code-panel">', unsafe_allow_html=True)
        st.markdown('<div class="code-header">Código de Salida - Python</div>', unsafe_allow_html=True)

        cols = st.columns([1, 2, 1])
        with cols[1]:
            convert_btn = st.button("CONVERTIR A PYTHON", use_container_width=True, type="primary")

        if convert_btn:
            if code_input.strip():
                # Normalizar idiomas
                norm_from = from_lang.lower().replace("c++", "cpp").replace("c#", "csharp")
                norm_to = to_lang.lower().replace("c++", "cpp").replace("c#", "csharp")
                with st.spinner(f"Traduciendo tu código de {from_lang} a {to_lang}..."):
                    translated = translator.translate(code_input, norm_from, norm_to)
                    entry = {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "from": from_lang,
                        "to": to_lang,
                        "input": code_input,
                        "output": translated
                    }
                    st.session_state.history.insert(0, entry)
                    if len(st.session_state.history) > 50:
                        st.session_state.history = st.session_state.history[:50]
                    st.session_state.translated_code = translated
                    st.session_state.translated_lang = norm_to
                    st.markdown(f'<div class="success-box">¡Código traducido a {to_lang} exitosamente!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">Por favor ingresa código para traducir</div>', unsafe_allow_html=True)

        if 'translated_code' in st.session_state:
            # Mapear lenguaje normalizado a highlighter de bloques de código
            code_lang_map = {
                'python': 'python', 'cpp': 'cpp', 'csharp': 'csharp', 'java': 'java', 'javascript': 'javascript',
                'ruby': 'ruby', 'go': 'go', 'rust': 'rust', 'php': 'php', 'typescript': 'typescript'
            }
            highlight = code_lang_map.get(st.session_state.get('translated_lang', 'python'), 'text')
            st.code(st.session_state.translated_code, language=highlight, line_numbers=True)

            if st.session_state.translated_code.strip():
                t_lines = len(st.session_state.translated_code.split('\n'))
                t_chars = len(st.session_state.translated_code)
                st.markdown(f"<small>{t_lines} líneas | {t_chars} caracteres</small>", unsafe_allow_html=True)

            col_down, col_copy = st.columns([1, 1])
            with col_down:
                ext_map_norm = {'python':'py','cpp':'cpp','csharp':'cs','java':'java','javascript':'js','ruby':'rb','go':'go','rust':'rs','php':'php','typescript':'ts'}
                lang_norm = st.session_state.get('translated_lang', 'python')
                fname = f"codigo_traducido.{ext_map_norm.get(lang_norm, 'txt')}"
                st.download_button(
                    "Descargar Código",
                    st.session_state.translated_code,
                    file_name=fname,
                    mime="text/plain",
                    use_container_width=True
                )
            with col_copy:
                if st.button("Copiar al Portapapeles", use_container_width=True):
                    st.success("Código copiado (usa Ctrl+C manualmente)")

            st.markdown("---")
            display_names = {'python':'Python','cpp':'C++','csharp':'C#','java':'Java','javascript':'JavaScript','ruby':'Ruby','go':'Go','rust':'Rust','php':'PHP','typescript':'TypeScript'}
            cur_lang = st.session_state.get('translated_lang', 'python')
            st.markdown(f"### Ejecutar Código {display_names.get(cur_lang, '')}")

            with st.expander("Configuración de Ejecución", expanded=False):
                stdin_input = st.text_area(
                    "Entrada estándar (stdin)",
                    height=100,
                    key="exec_stdin",
                    placeholder="Ingresa los datos de entrada aquí (uno por línea)\nEjemplo:\nJuan\n25",
                    help="Si tu código usa input() o similar, proporciona los valores aquí"
                )

            if (stdin_input is None or stdin_input.strip() == "") and st.session_state.translated_code.strip():
                suggested = auto_fill_for_ui(st.session_state.translated_code, cur_lang)
                if suggested:
                    st.info(f"Se autocompletarán entradas por defecto si no provees nada. Valores sugeridos:\n\n{suggested}")

            if st.button(f"EJECUTAR CÓDIGO {display_names.get(cur_lang, '').upper()}", use_container_width=True, type="primary"):
                if (st.session_state.get('exec_stdin', "") or "").strip() == "":
                    auto_stdin = auto_fill_for_ui(st.session_state.translated_code, cur_lang)
                    st.session_state.exec_stdin = auto_stdin

                with st.spinner("Ejecutando tu código..."):
                    success, output = run_translated_code(
                        st.session_state.translated_code,
                        cur_lang,
                        st.session_state.get('exec_stdin', "")
                    )
                    st.session_state.exec_output = output
                    st.session_state.exec_success = success

            if 'exec_output' in st.session_state:
                st.markdown("**Resultado de la Ejecución:**")
                if st.session_state.exec_success:
                    st.markdown('<div class="success-box">Ejecución exitosa</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">Error en la ejecución</div>', unsafe_allow_html=True)
                st.code(st.session_state.exec_output, language="bash")
        else:
            st.info("Ingresa tu código en la pestaña 'Entrada' y presiona **'CONVERTIR A PYTHON'** para ver la traducción aquí")

        st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## Historial de Conversiones")
       
        if st.button("Limpiar historial", use_container_width=True, key="clear_history"):
            st.session_state.history = []
            st.rerun()

        if len(st.session_state.history) > 0:
            history_text = "\n\n".join([
                f"=== {item['time']} ===\n{item['from']} → Python\n\nENTRADA:\n{item['input']}\n\nSALIDA:\n{item['output']}"
                for item in st.session_state.history
            ])
            st.download_button(
                "Descargar historial",
                history_text,
                file_name="historial_conversiones.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.markdown("---")
       
        if len(st.session_state.history) == 0:
            st.info("Aún no hay conversiones en el historial")
        else:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.history)}</div>
                <div class="stat-label">Conversiones a Python</div>
            </div>
            """, unsafe_allow_html=True)
           
            st.markdown("---")
           
            for idx, item in enumerate(st.session_state.history[:15]):
                with st.expander(
                    f"{item['from']} → Python | {item['time'].split()[1]}",
                    expanded=False
                ):
                    st.markdown(f"**Fecha:** {item['time']}")
                    st.markdown(f"**Conversión:** {item['from']} → Python")
                   
                    st.markdown(f"**Entrada ({item['from']}):**")
                    preview_in = item['input'][:150] + ("..." if len(item['input']) > 150 else "")
                    st.code(preview_in, language="text")
                   
                    st.markdown("**Salida (Python):**")
                    preview_out = item['output'][:150] + ("..." if len(item['output']) > 150 else "")
                    st.code(preview_out, language="python")
                   
                    col1, col2 = st.columns(2)
                    if col1.button("Cargar", key=f"load_{idx}", use_container_width=True):
                        st.session_state.code_input = item['input']
                        st.session_state.translated_code = item['output']
                        st.rerun()
                    if col2.button("Reusar", key=f"reuse_{idx}", use_container_width=True):
                        st.session_state.code_input = item['output']
                        if 'translated_code' in st.session_state:
                            del st.session_state.translated_code
                        st.rerun()

def get_file_extension(lang):
    ext_map = {
        "Python": "py",
        "C++": "cpp",
        "C#": "cs",
        "Java": "java",
        "JavaScript": "js",
        "Ruby": "rb",
        "Go": "go",
        "Rust": "rs",
        "PHP": "php",
        "TypeScript": "ts"
    }
    return ext_map.get(lang, "txt")

if __name__ == "__main__":
    main()
