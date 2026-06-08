import plotly.graph_objects as go

def get_tree_layout(node, tnull=None, x=0., y=0., dx=1.0, dy=-1.0, positions=None):
    if positions is None:
        positions = {}
    if node is None or node == tnull:
        return positions
    
    positions[node] = (x, y)
    if getattr(node, 'left', None) not in (None, tnull):
        get_tree_layout(node.left, tnull, x - dx/2, y + dy, dx/2, dy, positions)
    if getattr(node, 'right', None) not in (None, tnull):
        get_tree_layout(node.right, tnull, x + dx/2, y + dy, dx/2, dy, positions)
    return positions

def render_plotly_tree(tree, tree_type="AVL"):
    tnull = getattr(tree, 'TNULL', None)
    positions = get_tree_layout(tree.root, tnull, x=0.0, y=0.0, dx=1.0, dy=-1.0)
    
    fig = go.Figure()
    
    if not positions:
        fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig
        
    edge_x = []
    edge_y = []
    for node, (x, y) in positions.items():
        if getattr(node, 'left', None) not in (None, tnull):
            x0, y0 = positions[node]
            x1, y1 = positions[node.left]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        if getattr(node, 'right', None) not in (None, tnull):
            x0, y0 = positions[node]
            x1, y1 = positions[node.right]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#7F8C8D'),
        hoverinfo='none',
        mode='lines'
    ))

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node, (x, y) in positions.items():
        node_x.append(x)
        node_y.append(y)
        if tree_type == "AVL":
            balance = tree.get_balance(node)
            node_text.append(f"<b>{node.value}</b><br>B:{balance}")
            node_color.append('#2C3E50')
        else:
            node_text.append(f"<b>{node.value}</b>")
            color = '#E74C3C' if getattr(node, 'color', '') == 'RED' else '#2C3E50'
            node_color.append(color)

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="middle center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=45,
            line_width=2,
            line_color='white'
        ),
        textfont=dict(color='white', size=12)
    ))
    
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=20,r=20,t=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400 # Default height
    )
    
    return fig

def render_avl(tree):
    return render_plotly_tree(tree, "AVL")

def render_rbt(tree):
    return render_plotly_tree(tree, "RBT")
