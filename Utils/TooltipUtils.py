import Styles.colors as cl

def getTooltipHTML(title: str, description: str) -> str:
    return f"""
    <div style='background-color:{cl.SYS_BG2};'>
        <div style='background-color:{cl.SYS_BG2};color:{cl.SYS_FG1};font-weight:bold;font-size:12px;'>{title}</div>
        <div style='background-color:{cl.SYS_BG2};color:{cl.SYS_FG2};font-size:9px;'>{description}</div>
    </div>
    """