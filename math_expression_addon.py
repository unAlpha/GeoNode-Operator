# ============================================================================
# Blender 几何节点数学表达式插件
# ============================================================================
# 在几何节点编辑器侧边栏提供表达式输入面板
# 无需每次修改代码，直接输入表达式即可创建节点组
# ============================================================================

bl_info = {
    "name": "几何节点数学表达式",
    "author": "pdsharing.com",
    "version": (2, 0, 0),
    "blender": (3, 0, 0),
    "location": "几何节点编辑器 > 侧边栏 (N) > Math Expression",
    "description": "将数学表达式自动转换为几何节点组",
    "category": "Node",
}

import bpy
import ast
import re
from mathutils import Vector

# ============================================================================
# 核心功能代码（从原始脚本移植）
# ============================================================================

# 数学常量
MATH_CONSTANTS = {
    "pi": 3.1415927,
    "e": 2.7182818,
    "tau": 6.2831853,
    "phi": 1.6180339,
}

NODE_X_OFFSET = 200
NODE_Y_OFFSET = 80

# 单参数函数映射
UNARY_OPERATIONS = {
    "sin": "SINE",
    "cos": "COSINE",
    "tan": "TANGENT",
    "asin": "ARCSINE",
    "acos": "ARCCOSINE",
    "atan": "ARCTANGENT",
    "sinh": "SINH",
    "cosh": "COSH",
    "tanh": "TANH",
    "sqrt": "SQRT",
    "exp": "EXPONENT",
    "log": "LOGARITHM",
    "abs": "ABSOLUTE",
    "floor": "FLOOR",
    "ceil": "CEIL",
    "round": "ROUND",
    "frac": "FRACT",
    "trunc": "TRUNC",
    "sign": "SIGN",
    "radians": "RADIANS",
    "degrees": "DEGREES",
    "neg": "MULTIPLY",
}

# 双参数函数映射
BINARY_OPERATIONS = {
    "pow": "POWER",
    "mod": "MODULO",
    "min": "MINIMUM",
    "max": "MAXIMUM",
    "atan2": "ARCTAN2",
    "snap": "SNAP",
    "pingpong": "PINGPONG",
    "floordiv": "FLOORED_MODULO",
}

# 三参数函数映射
TERNARY_OPERATIONS = {
    "clamp": "CLAMP",
    "wrap": "WRAP",
    "smoothstep": "SMOOTH_MIN",
    "compare": "COMPARE",
}

# 运算符映射
OPERATOR_MAPPING = {
    "add": "ADD",
    "sub": "SUBTRACT",
    "mult": "MULTIPLY",
    "div": "DIVIDE",
    "pow": "POWER",
    "mod": "MODULO",
    "floordiv": "FLOORED_MODULO",
}


def link_sockets(from_socket, to_socket, node_tree):
    """连接两个套接字"""
    node_tree.links.new(from_socket, to_socket)


def create_math_node(node_tree, operation, location=(0, 0)):
    """创建数学节点"""
    node = node_tree.nodes.new("ShaderNodeMath")
    node.operation = operation
    node.location = location
    node.use_clamp = False
    return node


def create_value_node(node_tree, value, location=(0, 0), name=None):
    """创建数值常量节点"""
    node = node_tree.nodes.new("ShaderNodeValue")
    node.outputs[0].default_value = float(value)
    node.location = location
    if name:
        node.label = name
        node.name = name
    return node


class MathExpressionTransformer(ast.NodeTransformer):
    """AST 转换器：将数学表达式转换为函数调用"""

    def visit_BinOp(self, node):
        self.generic_visit(node)

        op_map = {
            ast.Add: "add",
            ast.Sub: "sub",
            ast.Mult: "mult",
            ast.Div: "div",
            ast.Pow: "pow",
            ast.Mod: "mod",
            ast.FloorDiv: "floordiv",
        }

        op_type = type(node.op)
        if op_type not in op_map:
            raise ValueError(f"不支持的运算符: {op_type.__name__}")

        func_name = op_map[op_type]

        return ast.Call(
            func=ast.Name(id=func_name, ctx=ast.Load()),
            args=[node.left, node.right],
            keywords=[],
        )

    def visit_UnaryOp(self, node):
        self.generic_visit(node)

        if isinstance(node.op, ast.USub):
            return ast.Call(
                func=ast.Name(id="neg", ctx=ast.Load()),
                args=[node.operand],
                keywords=[],
            )
        elif isinstance(node.op, ast.UAdd):
            return node.operand

        return node


class NodeTreeBuilder:
    """将解析后的 AST 转换为 Blender 几何节点树"""

    def __init__(self, node_tree):
        self.node_tree = node_tree
        self.current_x = 0
        self.current_y = 0
        self.node_count = 0
        self.variable_sockets = {}
        self.constant_nodes = {}

    def get_next_location(self):
        loc = (self.current_x, self.current_y)
        self.current_x += NODE_X_OFFSET
        self.current_y -= NODE_Y_OFFSET
        self.node_count += 1
        return loc

    def create_unary_node(self, operation, arg_socket):
        loc = self.get_next_location()
        node = create_math_node(self.node_tree, operation, loc)

        if operation == "MULTIPLY":  # neg
            node.inputs[1].default_value = -1.0

        link_sockets(arg_socket, node.inputs[0], self.node_tree)
        return node.outputs[0]

    def create_binary_node(self, operation, arg1_socket, arg2_socket):
        loc = self.get_next_location()
        node = create_math_node(self.node_tree, operation, loc)

        if isinstance(arg1_socket, bpy.types.NodeSocket):
            link_sockets(arg1_socket, node.inputs[0], self.node_tree)
        else:
            node.inputs[0].default_value = float(arg1_socket)

        if isinstance(arg2_socket, bpy.types.NodeSocket):
            link_sockets(arg2_socket, node.inputs[1], self.node_tree)
        else:
            node.inputs[1].default_value = float(arg2_socket)

        return node.outputs[0]

    def create_ternary_node(self, operation, arg1, arg2, arg3):
        loc = self.get_next_location()

        if operation == "CLAMP":
            node = self.node_tree.nodes.new("ShaderNodeClamp")
            node.location = loc
            inputs = [node.inputs[0], node.inputs[1], node.inputs[2]]
        else:
            node = create_math_node(self.node_tree, operation, loc)
            inputs = [node.inputs[0], node.inputs[1], node.inputs[2]]

        args = [arg1, arg2, arg3]
        for i, (inp, arg) in enumerate(zip(inputs, args)):
            if isinstance(arg, bpy.types.NodeSocket):
                link_sockets(arg, inp, self.node_tree)
            else:
                inp.default_value = float(arg)

        return node.outputs[0]

    def get_or_create_constant(self, value):
        key = str(value)
        if key not in self.constant_nodes:
            loc = self.get_next_location()
            node = create_value_node(self.node_tree, value, loc, f"C|{value}")
            self.constant_nodes[key] = node.outputs[0]
        return self.constant_nodes[key]

    def evaluate(self, node):
        if isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name is None:
                raise ValueError("不支持的函数调用形式")

            args = [self.evaluate(arg) for arg in node.args]

            if func_name in OPERATOR_MAPPING:
                operation = OPERATOR_MAPPING[func_name]
                return self.create_binary_node(operation, args[0], args[1])

            elif func_name == "neg":
                return self.create_unary_node("MULTIPLY", args[0])

            elif func_name in UNARY_OPERATIONS:
                operation = UNARY_OPERATIONS[func_name]
                return self.create_unary_node(operation, args[0])

            elif func_name in BINARY_OPERATIONS:
                operation = BINARY_OPERATIONS[func_name]
                return self.create_binary_node(operation, args[0], args[1])

            elif func_name in TERNARY_OPERATIONS or func_name == "clamp":
                if func_name == "clamp":
                    return self.create_ternary_node("CLAMP", args[0], args[1], args[2])
                operation = TERNARY_OPERATIONS[func_name]
                return self.create_ternary_node(operation, args[0], args[1], args[2])

            else:
                raise ValueError(f"未知函数: {func_name}")

        elif isinstance(node, ast.Name):
            var_name = node.id

            if var_name.lower() in MATH_CONSTANTS:
                return self.get_or_create_constant(MATH_CONSTANTS[var_name.lower()])

            if var_name not in self.variable_sockets:
                raise ValueError(f"未定义的变量: {var_name}")

            return self.variable_sockets[var_name]

        elif isinstance(node, ast.Constant):
            return self.get_or_create_constant(node.value)

        elif isinstance(node, ast.Num):
            return self.get_or_create_constant(node.n)

        else:
            raise ValueError(f"不支持的 AST 节点类型: {type(node).__name__}")


def extract_variables(expression):
    """从表达式中提取所有变量名"""
    tree = ast.parse(expression, mode="eval")

    variables = set()
    known_functions = (
        set(UNARY_OPERATIONS.keys())
        | set(BINARY_OPERATIONS.keys())
        | set(TERNARY_OPERATIONS.keys())
        | {"clamp", "neg"}
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            name = node.id
            if name not in known_functions and name.lower() not in MATH_CONSTANTS:
                variables.add(name)

    return sorted(variables)


def create_expression_nodegroup(expression, node_group_name="MathExpression"):
    """从数学表达式创建几何节点组"""

    print(f"解析表达式: {expression}")

    # 提取变量
    variables = extract_variables(expression)
    print(f"发现变量: {variables}")

    # 创建或获取节点组
    if node_group_name in bpy.data.node_groups:
        ng = bpy.data.node_groups[node_group_name]
        ng.nodes.clear()
    else:
        ng = bpy.data.node_groups.new(name=node_group_name, type="GeometryNodeTree")

    # 清除现有接口
    ng.interface.clear()

    # 创建输入/输出套接字
    ng.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    ng.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )

    for var in variables:
        ng.interface.new_socket(name=var, in_out="INPUT", socket_type="NodeSocketFloat")

    ng.interface.new_socket(
        name="Result", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )

    # 创建输入输出节点
    input_node = ng.nodes.new("NodeGroupInput")
    input_node.location = (-400, 0)

    output_node = ng.nodes.new("NodeGroupOutput")
    output_node.location = (800, 0)

    ng.links.new(input_node.outputs["Geometry"], output_node.inputs["Geometry"])

    # 解析并转换表达式
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"表达式语法错误: {e}")

    transformer = MathExpressionTransformer()
    transformed = transformer.visit(tree.body)

    # 构建节点树
    builder = NodeTreeBuilder(ng)

    for var in variables:
        builder.variable_sockets[var] = input_node.outputs[var]

    result_socket = builder.evaluate(transformed)

    if result_socket:
        ng.links.new(result_socket, output_node.inputs["Result"])

    output_node.location = (builder.current_x + 200, 0)

    # 存储原始表达式和创建标记（用于后续识别和加载）
    ng["math_expr_original"] = expression
    ng["math_expr_created_by"] = "math_expression_addon"

    print(f"成功创建节点组 '{node_group_name}'，包含 {builder.node_count} 个数学节点")

    return ng


# ============================================================================
# Blender 插件代码
# ============================================================================


def get_math_expression_node_groups():
    """获取所有由本插件创建的节点组"""
    result = []
    for ng in bpy.data.node_groups:
        if ng.bl_idname == "GeometryNodeTree" and "math_expr_created_by" in ng:
            if ng["math_expr_created_by"] == "math_expression_addon":
                result.append(ng)
    return result


class MATHEXP_OT_CreateNodeGroup(bpy.types.Operator):
    """创建数学表达式节点组"""

    bl_idname = "node.math_expression_create"
    bl_label = "创建节点组"
    bl_description = "根据表达式创建几何节点组"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = context.scene.math_expression_props

        if not props.expression:
            self.report({"ERROR"}, "请输入表达式")
            return {"CANCELLED"}

        if not props.node_group_name:
            self.report({"ERROR"}, "请输入节点组名称")
            return {"CANCELLED"}

        try:
            ng = create_expression_nodegroup(props.expression, props.node_group_name)

            # 自动添加到当前节点树中
            if context.space_data and context.space_data.type == "NODE_EDITOR":
                node_tree = context.space_data.edit_tree
                if node_tree and node_tree.bl_idname == "GeometryNodeTree":
                    # 创建节点组节点
                    group_node = node_tree.nodes.new("GeometryNodeGroup")
                    group_node.node_tree = ng

                    # 将节点放置在视图中心
                    # 获取视图的中心坐标
                    region = context.region
                    view2d = context.region.view2d
                    # 将区域中心转换为节点编辑器坐标
                    center_x = region.width / 2.0
                    center_y = region.height / 2.0
                    node_location = view2d.region_to_view(center_x, center_y)
                    group_node.location = node_location

                    group_node.select = True
                    # 取消其他节点的选择
                    for node in node_tree.nodes:
                        if node != group_node:
                            node.select = False
                    # 设置为活动节点
                    node_tree.nodes.active = group_node

            self.report({"INFO"}, f"成功创建节点组 '{props.node_group_name}'")

            # 清空表达式（可选）
            if props.clear_after_create:
                props.expression = ""

            return {"FINISHED"}

        except Exception as e:
            self.report({"ERROR"}, f"创建失败: {str(e)}")
            return {"CANCELLED"}


class MATHEXP_OT_UpdateNodeGroup(bpy.types.Operator):
    """更新已存在的数学表达式节点组"""

    bl_idname = "node.math_expression_update"
    bl_label = "更新节点组"
    bl_description = "更新已存在的几何节点组"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        props = context.scene.math_expression_props
        return props.node_group_name in bpy.data.node_groups

    def execute(self, context):
        props = context.scene.math_expression_props

        if not props.expression:
            self.report({"ERROR"}, "请输入表达式")
            return {"CANCELLED"}

        if not props.node_group_name:
            self.report({"ERROR"}, "请输入节点组名称")
            return {"CANCELLED"}

        if props.node_group_name not in bpy.data.node_groups:
            self.report({"ERROR"}, f"节点组 '{props.node_group_name}' 不存在")
            return {"CANCELLED"}

        try:
            ng = create_expression_nodegroup(props.expression, props.node_group_name)
            self.report({"INFO"}, f"成功更新节点组 '{props.node_group_name}'")

            # 清空表达式（可选）
            if props.clear_after_create:
                props.expression = ""

            return {"FINISHED"}

        except Exception as e:
            self.report({"ERROR"}, f"更新失败: {str(e)}")
            return {"CANCELLED"}


class MATHEXP_OT_DeleteNodeGroup(bpy.types.Operator):
    """删除数学表达式节点组"""

    bl_idname = "node.math_expression_delete"
    bl_label = "删除节点组"
    bl_description = "从工程中删除指定的节点组"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        props = context.scene.math_expression_props
        return props.node_group_name in bpy.data.node_groups

    def invoke(self, context, event):
        # 弹出确认对话框
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        props = context.scene.math_expression_props

        if not props.node_group_name:
            self.report({"ERROR"}, "请输入节点组名称")
            return {"CANCELLED"}

        if props.node_group_name not in bpy.data.node_groups:
            self.report({"ERROR"}, f"节点组 '{props.node_group_name}' 不存在")
            return {"CANCELLED"}

        try:
            ng = bpy.data.node_groups[props.node_group_name]
            ng_name = ng.name  # 保存名称用于报告

            # 从当前节点树中删除所有使用该节点组的节点
            removed_count = 0
            if context.space_data and context.space_data.type == "NODE_EDITOR":
                node_tree = context.space_data.edit_tree
                if node_tree and node_tree.bl_idname == "GeometryNodeTree":
                    nodes_to_remove = []
                    for node in node_tree.nodes:
                        if node.type == "GROUP" and node.node_tree == ng:
                            nodes_to_remove.append(node)

                    for node in nodes_to_remove:
                        node_tree.nodes.remove(node)
                        removed_count += 1

            # 从工程中删除节点组
            bpy.data.node_groups.remove(ng)

            if removed_count > 0:
                self.report(
                    {"INFO"},
                    f"成功删除节点组 '{ng_name}' 及场景中的 {removed_count} 个实例",
                )
            else:
                self.report({"INFO"}, f"成功删除节点组 '{ng_name}'")

            return {"FINISHED"}

        except Exception as e:
            self.report({"ERROR"}, f"删除失败: {str(e)}")
            return {"CANCELLED"}


class MATHEXP_PT_Panel(bpy.types.Panel):
    """几何节点编辑器侧边栏面板"""

    bl_label = "Math Expression"
    bl_idname = "MATHEXP_PT_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Math"
    bl_context = ""

    @classmethod
    def poll(cls, context):
        # 只在几何节点编辑器中显示
        return context.space_data.tree_type == "GeometryNodeTree"

    def draw(self, context):
        layout = self.layout
        props = context.scene.math_expression_props

        # 检查节点组是否存在
        node_group_exists = props.node_group_name in bpy.data.node_groups

        # 表达式输入
        box = layout.box()
        box.label(text="表达式:", icon="SYNTAX_ON")
        box.prop(props, "expression", text="")

        # 节点组名称和清空按钮
        row = box.row(align=True)
        row.prop(props, "node_group_name", text="名称")
        row.operator("node.math_expression_clear", text="", icon="X")

        # 节点组状态提示
        if node_group_exists:
            status_row = box.row()
            status_row.alert = False
            status_row.label(text="节点组已存在", icon="CHECKMARK")

        # 创建/更新按钮
        row = box.row()
        row.scale_y = 1.5

        if node_group_exists:
            # 如果节点组存在，只显示更新按钮
            row.operator(
                "node.math_expression_update", text="更新节点组", icon="FILE_REFRESH"
            )
        else:
            # 如果不存在，只显示创建按钮
            row.operator("node.math_expression_create", text="创建节点组", icon="ADD")

        # 删除按钮（仅在节点组存在时显示）
        if node_group_exists:
            delete_row = box.row()
            delete_row.scale_y = 1.2
            delete_row.alert = True  # 使用警告颜色（红色）
            delete_row.operator(
                "node.math_expression_delete", text="删除节点组", icon="TRASH"
            )

        # 选项
        box.prop(props, "clear_after_create", text="创建后清空表达式")

        # 节点组列表
        layout.separator()
        box = layout.box()

        # 获取所有由工具创建的节点组
        math_node_groups = get_math_expression_node_groups()

        if math_node_groups:
            box.label(
                text=f"已创建的节点组 ({len(math_node_groups)}):", icon="NODETREE"
            )

            # 节点组列表
            col = box.column(align=True)
            for ng in math_node_groups:
                row = col.row(align=True)
                row.scale_y = 1.1

                # 节点组加载按钮
                op = row.operator(
                    "node.math_expression_load", text=ng.name, icon="NODE"
                )
                op.node_group_name = ng.name

                # 显示表达式预览（如果有）
                if "math_expr_original" in ng:
                    expr = ng["math_expr_original"]
                    # 截断过长的表达式
                    if len(expr) > 30:
                        expr_preview = expr[:27] + "..."
                    else:
                        expr_preview = expr
                    row.label(text=f"  {expr_preview}")
        else:
            box.label(text="暂无创建的节点组", icon="INFO")

        # 快速示例（可折叠）
        layout.separator()
        box = layout.box()

        # 折叠标题行
        row = box.row()
        row.prop(
            props,
            "show_examples",
            icon="TRIA_DOWN" if props.show_examples else "TRIA_RIGHT",
            icon_only=True,
            emboss=False,
        )
        row.label(text="快速示例", icon="PRESET")

        # 展开时显示示例列表
        if props.show_examples:
            col = box.column(align=True)

            examples = [
                ("a + b", "简单加法", "ADD"),
                ("sin(x) * a", "正弦波", "FCURVE"),
                ("sqrt(x**2 + y**2)", "距离", "DRIVER_DISTANCE"),
                ("clamp(x, 0, 1)", "限制范围", "CLIPUV_DEHLT"),
                ("1 / (1 + exp(-x))", "Sigmoid", "IPO_EASE_IN_OUT"),
            ]

            for expr, desc, icon in examples:
                row = col.row(align=True)
                row.scale_y = 1.2

                # 示例按钮
                op = row.operator("node.math_expression_insert", text=desc, icon=icon)
                op.expression = expr


class MATHEXP_OT_InsertExample(bpy.types.Operator):
    """插入示例表达式"""

    bl_idname = "node.math_expression_insert"
    bl_label = "插入示例"
    bl_description = "插入示例表达式"

    expression: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.math_expression_props.expression = self.expression
        return {"FINISHED"}


class MATHEXP_OT_ClearFields(bpy.types.Operator):
    """清空表达式和名称"""

    bl_idname = "node.math_expression_clear"
    bl_label = "清空"
    bl_description = "清空表达式和节点组名称"

    def execute(self, context):
        props = context.scene.math_expression_props
        props.expression = ""
        props.node_group_name = "MathExpression"
        self.report({"INFO"}, "已清空表达式和名称")
        return {"FINISHED"}


class MATHEXP_OT_LoadNodeGroup(bpy.types.Operator):
    """从节点组加载表达式"""

    bl_idname = "node.math_expression_load"
    bl_label = "加载节点组"
    bl_description = "从选择的节点组加载表达式和名称"

    node_group_name: bpy.props.StringProperty()

    def execute(self, context):
        props = context.scene.math_expression_props

        if self.node_group_name not in bpy.data.node_groups:
            self.report({"ERROR"}, f"节点组 '{self.node_group_name}' 不存在")
            return {"CANCELLED"}

        ng = bpy.data.node_groups[self.node_group_name]

        # 加载表达式（如果存储了）
        if "math_expr_original" in ng:
            props.expression = ng["math_expr_original"]
            props.node_group_name = ng.name
            self.report({"INFO"}, f"已加载节点组 '{ng.name}'")
        else:
            # 如果没有存储表达式，只加载名称
            props.node_group_name = ng.name
            props.expression = ""
            self.report({"WARNING"}, f"节点组 '{ng.name}' 没有存储表达式信息")

        return {"FINISHED"}


class MathExpressionProperties(bpy.types.PropertyGroup):
    """插件属性"""

    expression: bpy.props.StringProperty(
        name="表达式", description="数学表达式，如: sin(x) * a + cos(y) * b", default=""
    )

    node_group_name: bpy.props.StringProperty(
        name="节点组名称", description="创建的节点组名称", default="MathExpression"
    )

    clear_after_create: bpy.props.BoolProperty(
        name="创建后清空", description="创建节点组后清空表达式输入框", default=False
    )

    show_examples: bpy.props.BoolProperty(
        name="显示快速示例", description="显示或隐藏快速示例列表", default=False
    )


# ============================================================================
# 注册和注销
# ============================================================================

classes = (
    MathExpressionProperties,
    MATHEXP_OT_CreateNodeGroup,
    MATHEXP_OT_UpdateNodeGroup,
    MATHEXP_OT_DeleteNodeGroup,
    MATHEXP_OT_InsertExample,
    MATHEXP_OT_ClearFields,
    MATHEXP_OT_LoadNodeGroup,
    MATHEXP_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.math_expression_props = bpy.props.PointerProperty(
        type=MathExpressionProperties
    )

    print("几何节点数学表达式插件已加载")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.math_expression_props

    print("几何节点数学表达式插件已卸载")


if __name__ == "__main__":
    register()
