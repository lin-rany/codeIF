import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz
def draw_dependency_graph(dependence_map):
    # 创建有向图
    G = nx.DiGraph()
    G.add_nodes_from(dependence_map.keys())
    for node, deps in dependence_map.items():
        for dep in deps:
            G.add_edge(node, dep)
    
    # 使用graphviz的dot布局，适合层次结构
    pos = graphviz_layout(G, prog='dot')
    
    # 绘制图形
    plt.figure(figsize=(12, 12))  # 调整图形大小
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=10, arrows=True, node_color="lightblue")
    
    # 显示图形
    plt.show()