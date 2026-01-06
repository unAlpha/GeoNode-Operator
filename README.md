# 几何节点数学表达式插件

> 在 Blender 几何节点编辑器中，通过输入数学表达式自动生成节点组

## 项目简介

这是一个轻量级 Blender 插件，可以将数学表达式（如 `sin(x) * a + cos(y) * b`）自动转换为几何节点组。无需手工创建和连接大量数学节点，只需输入公式即可。

### 特点

- 🎯 **简单易用** - 在侧边栏输入表达式，一键创建
- 🚀 **功能强大** - 支持 30+ 种数学函数和运算符
- 💡 **所见即所得** - 自动识别变量，创建输入套接字
- 📦 **轻量级** - 单文件插件，无外部依赖

### 快速开始

```python
# 1. 安装插件（三种方式任选其一）
#    - 偏好设置 → 插件 → 安装
#    - 或直接在脚本编辑器运行（临时）

# 2. 打开几何节点编辑器，按 N 键

# 3. 在 Math 选项卡输入表达式
表达式: sin(x * 2 * pi) * amplitude
名称: WaveEffect

# 4. 点击"创建节点组"按钮

# 5. 在节点树中添加这个节点组（Shift+A → 群组）
```

---

## 安装和使用指南

## 插件安装

### 方法 1: 通过 Blender 界面安装

1. 打开 Blender
2. 进入 **编辑 (Edit) > 偏好设置 (Preferences)**
3. 选择 **插件 (Add-ons)** 选项卡
4. 点击右上角 **安装 (Install)** 按钮
5. 选择 `math_expression_addon.py` 文件
6. 勾选启用插件 "几何节点数学表达式"

### 方法 2: 直接复制到插件目录

将 `math_expression_addon.py` 复制到 Blender 插件目录：
- **Windows**: `%APPDATA%\Blender Foundation\Blender\<版本>\scripts\addons\`
- **macOS**: `~/Library/Application Support/Blender/<版本>/scripts/addons/`
- **Linux**: `~/.config/blender/<版本>/scripts/addons/`

然后在偏好设置中启用插件。

### 方法 3: 临时使用（无需安装）

1. 在 Blender 脚本编辑器中打开 `math_expression_addon.py`
2. 点击"运行脚本"按钮（或按 `Alt + P`）
3. 插件将在当前会话中激活（重启 Blender 后需要重新运行）

## 使用方法

### 1. 打开插件面板

1. 切换到**几何节点编辑器** (Geometry Node Editor)
2. 按 **N 键**打开侧边栏
3. 找到 **Math** 选项卡
4. 展开 **Math Expression** 面板

### 2. 创建节点组

**方式 A: 手动输入**
1. 在"表达式"框中输入您的数学表达式
   - 例如: `sin(x) * a + cos(y) * b`
2. 在"名称"框中输入节点组名称
   - 例如: `MyFormula`
3. 点击 **创建节点组** 按钮

**方式 B: 使用快速示例**
1. 点击任意示例按钮（如"简单加法"）
2. 表达式会自动填充到输入框
3. 点击 **创建节点组** 按钮

### 3. 使用创建的节点组

1. 在几何节点编辑器中按 **Shift + A**
2. 选择 **群组 (Group)** → 找到您创建的节点组
3. 连接输入变量和几何体
4. 使用 **Result** 输出

## 插件界面说明

```
┌─────────────────────────────┐
│ Math Expression             │
├─────────────────────────────┤
│ 表达式:                     │
│ ┌─────────────────────────┐ │
│ │ sin(x) * a + cos(y) * b │ │  ← 输入表达式
│ └─────────────────────────┘ │
│                             │
│ 名称: MathExpression        │  ← 节点组名称
│                             │
│ ┌─────────────────────────┐ │
│ │   创建节点组            │ │  ← 点击创建
│ └─────────────────────────┘ │
│                             │
│ ☐ 创建后清空表达式          │  ← 选项
│                             │
│ 快速示例:                   │
│ ┌─────────────────────────┐ │
│ │ 简单加法                │ │  ← 示例按钮
│ │ 正弦波                  │ │
│ │ 距离                    │ │
│ │ 限制范围                │ │
│ │ Sigmoid                 │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

## 支持的语法

### 运算符
- `+` `-` `*` `/` `**` `%` `//`
- 负号: `-x`

### 函数
**三角函数**: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`

**数学函数**: `sqrt`, `pow`, `exp`, `log`, `abs`, `sign`

**取整函数**: `floor`, `ceil`, `round`, `trunc`, `frac`

**实用函数**: `min`, `max`, `mod`, `clamp`, `snap`, `pingpong`, `wrap`, `radians`, `degrees`

### 常量
`pi`, `e`, `tau`, `phi`

### 变量
任意字母组合（如 `a`, `x`, `amplitude`, `frequency`）

## 示例表达式

```python
# 基础运算
"a + b"
"(a + b) / 2"

# 三角函数
"sin(x * 2 * pi)"
"amplitude * sin(frequency * x + phase)"

# 距离计算
"sqrt(x**2 + y**2)"
"sqrt(x**2 + y**2 + z**2)"

# 限制和映射
"clamp(x, 0, 1)"
"a * (1 - t) + b * t"

# 复杂表达式
"1 / (1 + exp(-x))"  # Sigmoid
"sin(sqrt(x**2 + y**2) * frequency - time) * amplitude"  # 涟漪
```

## 工作流程示例

### 示例 1: 创建波浪效果

1. 在侧边栏输入表达式:
   ```
   sin(x * frequency + time) * amplitude
   ```
2. 名称: `Wave`
3. 创建节点组
4. 在几何节点中:
   - 使用"位置"节点获取 x 坐标
   - 连接到 Wave 节点组的 `x` 输入
   - 添加"时间"节点连接到 `time`
   - 设置 `frequency` 和 `amplitude`
   - 将 `Result` 连接到"设置位置"的 Z 偏移

### 示例 2: 径向渐变

1. 输入表达式:
   ```
   sqrt(x**2 + y**2)
   ```
2. 名称: `RadialDistance`
3. 在几何节点中:
   - 分别提取位置的 X 和 Y
   - 连接到节点组
   - 使用结果作为颜色或缩放因子

### 示例 3: 自定义缓动曲线

1. 输入表达式:
   ```
   t**2 * (3 - 2 * t)
   ```
2. 名称: `SmoothStep`
3. 用于任何需要平滑过渡的地方

## 常见问题

**Q: 插件面板在哪里？**  
A: 在几何节点编辑器中按 N 键，找到 "Math" 选项卡。

**Q: 为什么节点组有 Geometry 输入输出？**  
A: 几何节点组必须有几何体接口。这是直通连接，不影响数学运算。

**Q: 可以修改已创建的节点组吗？**  
A: 使用相同的名称再次创建会覆盖旧节点组。

**Q: 表达式报错怎么办？**  
A: 检查语法是否正确，括号是否匹配，函数名是否正确。

**Q: 可以使用中文变量名吗？**  
A: 不可以，变量名必须是英文字母。

## 与独立脚本的对比

| 特性 | 独立脚本 | 轻量级插件 |
|------|----------|------------|
| 安装 | 无需安装 | 需要安装一次 |
| 使用便利性 | ⭐⭐ 每次需打开脚本修改 | ⭐⭐⭐⭐⭐ 侧边栏直接使用 |
| UI 界面 | ❌ 无 | ✅ 友好的输入面板 |
| 快速示例 | ❌ 无 | ✅ 一键插入 |
| 持久性 | ❌ 关闭 Blender 丢失 | ✅ 安装后永久可用 |

## 卸载插件

1. 进入 **编辑 > 偏好设置 > 插件**
2. 找到"几何节点数学表达式"
3. 取消勾选或点击"移除"按钮

---

## 实现原理

### 技术架构

插件使用 Python AST（抽象语法树）模块来解析和转换数学表达式，核心流程如下：

```
用户输入表达式
    ↓
提取变量 extract_variables()
    ↓
创建节点组和输入套接字
    ↓
AST 解析 ast.parse()
    ↓
表达式转换 MathExpressionTransformer
    ↓
递归构建节点 NodeTreeBuilder
    ↓
连接输出套接字
    ↓
完成的几何节点组
```

### 核心模块

#### 1. 表达式转换器 (MathExpressionTransformer)

使用 Python 的 `ast.NodeTransformer` 将中缀表达式转换为前缀函数调用：

```python
# 输入表达式
"a + b * 2"

# AST 解析
BinOp(left=Name('a'), op=Add(), right=BinOp(...))

# 转换为函数调用
Call(func=Name('add'), args=[
    Name('a'),
    Call(func=Name('mult'), args=[Name('b'), Constant(2)])
])

# 对应的函数表达式
"add(a, mult(b, 2))"
```

**转换规则**：
- 二元运算符 → 双参数函数：`a + b` → `add(a, b)`
- 一元运算符 → 单参数函数：`-x` → `neg(x)`
- 函数调用保持不变：`sin(x)` → `sin(x)`

#### 2. 变量提取器 (extract_variables)

遍历 AST 树，收集所有变量名：

```python
表达式: "sin(x) * a + cos(y) * b"
提取变量: ['a', 'b', 'x', 'y']  # 排除函数名(sin, cos)和常量
```

**识别逻辑**：
- 是 `ast.Name` 节点
- 不在函数名列表中
- 不在常量名列表中（pi, e, tau, phi）

#### 3. 节点树构建器 (NodeTreeBuilder)

递归遍历转换后的 AST，为每个函数调用创建对应的 `ShaderNodeMath` 节点：

```python
# 表达式: add(a, mult(b, 2))
#
# 构建过程（后序遍历）:
# 1. 处理 mult(b, 2)
#    - 创建 Math 节点（MULTIPLY 操作）
#    - 连接 b 输入套接字 → inputs[0]
#    - 设置常量 2 → inputs[1]
#    - 返回输出套接字
#
# 2. 处理 add(a, ...)
#    - 创建 Math 节点（ADD 操作）
#    - 连接 a 输入套接字 → inputs[0]
#    - 连接上一步的输出 → inputs[1]
#    - 返回输出套接字
#
# 3. 连接最终输出到 Group Output
```

**节点布局算法**：
- 从左到右横向排列
- 每创建一个节点，X 坐标增加 200
- Y 坐标递减 80（形成阶梯状）

### 关键函数说明

#### create_expression_nodegroup()

主函数，协调整个创建流程：

```python
def create_expression_nodegroup(expression, node_group_name):
    # 1. 提取变量
    variables = extract_variables(expression)
    
    # 2. 创建节点组
    ng = bpy.data.node_groups.new(...)
    
    # 3. 创建输入/输出套接字
    for var in variables:
        ng.interface.new_socket(name=var, ...)
    
    # 4. 解析表达式
    tree = ast.parse(expression, mode='eval')
    transformer = MathExpressionTransformer()
    transformed = transformer.visit(tree.body)
    
    # 5. 构建节点树
    builder = NodeTreeBuilder(ng)
    result_socket = builder.evaluate(transformed)
    
    # 6. 连接输出
    ng.links.new(result_socket, output_node.inputs['Result'])
    
    return ng
```

#### NodeTreeBuilder.evaluate()

递归评估 AST 节点：

```python
def evaluate(self, node):
    if isinstance(node, ast.Call):
        # 函数调用 - 创建相应的 Math 节点
        func_name = node.func.id
        args = [self.evaluate(arg) for arg in node.args]  # 递归评估参数
        return self.create_binary_node(operation, args[0], args[1])
    
    elif isinstance(node, ast.Name):
        # 变量引用 - 返回输入套接字
        return self.variable_sockets[node.id]
    
    elif isinstance(node, ast.Constant):
        # 常量 - 创建 Value 节点
        return self.get_or_create_constant(node.value)
```

### 数据流示例

完整示例：`sin(x) * a + cos(y) * b`

```
1. 变量提取
   变量: [a, b, x, y]

2. 创建输入套接字
   Group Input.a
   Group Input.b
   Group Input.x
   Group Input.y

3. AST 转换
   add(
       mult(sin(x), a),
       mult(cos(y), b)
   )

4. 节点构建（递归）
   
   Level 3: sin(x)
   ┌──────────────┐
   │ Math (SINE)  │ ← x
   └──────────────┘
         ↓
   Level 3: cos(y)
   ┌──────────────┐
   │ Math (COS)   │ ← y
   └──────────────┘
         ↓
   Level 2: mult(sin(x), a)
   ┌──────────────┐
   │ Math (MULT)  │ ← sin(x), a
   └──────────────┘
         ↓
   Level 2: mult(cos(y), b)
   ┌──────────────┐
   │ Math (MULT)  │ ← cos(y), b
   └──────────────┘
         ↓
   Level 1: add(...)
   ┌──────────────┐
   │ Math (ADD)   │ ← mult(...), mult(...)
   └──────────────┘
         ↓
   Group Output.Result

5. 最终节点树
   Group Input → sin → mult ┐
                            ├→ add → Group Output
   Group Input → cos → mult ┘
```

### 代码结构

```python
# ============ 核心功能 ============
class MathExpressionTransformer(ast.NodeTransformer):
    """AST 转换器"""
    def visit_BinOp(self, node):
        # 将 a + b 转换为 add(a, b)
        
    def visit_UnaryOp(self, node):
        # 将 -x 转换为 neg(x)

class NodeTreeBuilder:
    """节点树构建器"""
    def __init__(self, node_tree):
        self.node_tree = node_tree
        self.variable_sockets = {}
        self.constant_nodes = {}
    
    def evaluate(self, node):
        # 递归评估 AST 节点
    
    def create_binary_node(self, operation, arg1, arg2):
        # 创建双参数数学节点

def extract_variables(expression):
    """提取表达式中的变量"""

def create_expression_nodegroup(expression, name):
    """主创建函数"""

# ============ Blender 插件 ============
class MathExpressionProperties(bpy.types.PropertyGroup):
    """属性存储"""
    expression: StringProperty()
    node_group_name: StringProperty()

class MATHEXP_OT_CreateNodeGroup(bpy.types.Operator):
    """创建操作器"""
    def execute(self, context):
        create_expression_nodegroup(...)

class MATHEXP_PT_Panel(bpy.types.Panel):
    """UI 面板"""
    def draw(self, context):
        layout.prop(props, "expression")
        layout.operator("node.math_expression_create")
```

### 支持的操作映射

```python
# 运算符 → ShaderNodeMath 操作
OPERATOR_MAPPING = {
    'add': 'ADD',
    'sub': 'SUBTRACT',
    'mult': 'MULTIPLY',
    'div': 'DIVIDE',
    'pow': 'POWER',
    'mod': 'MODULO',
    'floordiv': 'FLOORED_MODULO',
}

# 函数 → ShaderNodeMath 操作
UNARY_OPERATIONS = {
    'sin': 'SINE',
    'cos': 'COSINE',
    'sqrt': 'SQRT',
    'abs': 'ABSOLUTE',
    # ... 30+ 种函数
}
```

### 扩展指南

如果您想添加新功能：

#### 添加新函数

1. 在 `UNARY_OPERATIONS` 或 `BINARY_OPERATIONS` 中添加映射
2. 确保 Blender 的 `ShaderNodeMath` 支持该操作

```python
# 例如添加新函数 "cube"（立方）
UNARY_OPERATIONS = {
    # ... 现有函数
    'cube': 'POWER',  # 需要特殊处理
}

# 在 evaluate() 中添加特殊处理
if func_name == 'cube':
    return self.create_binary_node('POWER', args[0], 3)
```

#### 添加向量支持

需要修改 `NodeTreeBuilder` 支持 `ShaderNodeVectorMath`：

```python
def create_vector_node(self, operation, arg1, arg2):
    node = node_tree.nodes.new('ShaderNodeVectorMath')
    node.operation = operation
    # ... 连接逻辑
```

#### 添加表达式验证

在 `MATHEXP_PT_Panel.draw()` 中添加实时验证：

```python
def draw(self, context):
    # ... 现有代码
    
    # 验证表达式
    if props.expression:
        try:
            ast.parse(props.expression, mode='eval')
            # 显示绿色勾号
        except SyntaxError:
            # 显示红色警告
```

## 技术支持

- 查看源代码获取更多细节
- 代码注释详细，易于理解和修改
- 欢迎提出改进建议
