from typing import Any
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

server = Server("weather")
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    列出可用的工具。
    每个工具使用 JSON Schema 验证来指定其参数。
    """
    return [
        types.Tool(
            name="get-alerts",
            description="获取某个州的天气预警",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "两字母州代码(如 CA, NY)",
                    },
                },
                "required": ["state"],
            },
        ),
        types.Tool(
            name="get-forecast",
            description="获取某个位置的天气预报",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "位置的纬度",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "位置的经度",
                    },
                },
                "required": ["latitude", "longitude"],
            },
        ),
    ]
async def make_nws_request(client: httpx.AsyncClient, url: str) -> dict[str, Any] | None:
    """发送 NWS API 请求并进行适当的错误处理。"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    try:
        response = await client.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

def format_alert(feature: dict) -> str:
    """将预警特征格式化为简明的字符串。"""
    props = feature["properties"]
    return (
        f"事件: {props.get('event', '未知')}\n"
        f"区域: {props.get('areaDesc', '未知')}\n"
        f"严重程度: {props.get('severity', '未知')}\n"
        f"状态: {props.get('status', '未知')}\n"
        f"标题: {props.get('headline', '无标题')}\n"
        "---"
    )

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    处理工具执行请求。
    工具可以获取天气数据并通知客户端变更。
    """
    if not arguments:
        raise ValueError("缺少参数")
  
    if name == "get-alerts":
        state = arguments.get("state")
        if not state:
            raise ValueError("缺少州参数")

        # 转换州代码为大写以确保格式一致
        state = state.upper()
        if len(state) != 2:
            raise ValueError("州必须是两字母代码(如 CA, NY)")

        async with httpx.AsyncClient() as client:
            alerts_url = f"{NWS_API_BASE}/alerts?area={state}"
            alerts_data = await make_nws_request(client, alerts_url)

            if not alerts_data:
                return [types.TextContent(type="text", text="获取预警数据失败")]

            features = alerts_data.get("features", [])
            if not features:
                return [types.TextContent(type="text", text=f"{state} 没有活动预警")]

            # 格式化每个预警为简明字符串
            formatted_alerts = [format_alert(feature) for feature in features[:20]]  # 仅取前20个预警
            alerts_text = f"{state} 的活动预警:\n\n" + "\n".join(formatted_alerts)

            return [
                types.TextContent(
                    type="text",
                    text=alerts_text
                )
            ]
    elif name == "get-forecast":
        try:
            latitude = float(arguments.get("latitude"))
            longitude = float(arguments.get("longitude"))
        except (TypeError, ValueError):
            return [types.TextContent(
                type="text",
                text="无效的坐标。请提供有效的纬度和经度数值。"
            )]
            
        # 基本坐标验证
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            return [types.TextContent(
                type="text",
                text="无效的坐标。纬度必须在 -90 到 90 之间,经度必须在 -180 到 180 之间。"
            )]

        async with httpx.AsyncClient() as client:
            # 首先获取网格点
            lat_str = f"{latitude}"
            lon_str = f"{longitude}"
            points_url = f"{NWS_API_BASE}/points/{lat_str},{lon_str}"
            points_data = await make_nws_request(client, points_url)

            if not points_data:
                return [types.TextContent(type="text", text=f"无法获取坐标 {latitude}, {longitude} 的网格点数据。此位置可能不受 NWS API 支持(仅支持美国地点)。")]

            # 从响应中提取预报 URL
            properties = points_data.get("properties", {})
            forecast_url = properties.get("forecast")
            
            if not forecast_url:
                return [types.TextContent(type="text", text="无法从网格点数据获取预报 URL")]

            # 获取预报
            forecast_data = await make_nws_request(client, forecast_url)
            
            if not forecast_data:
                return [types.TextContent(type="text", text="获取预报数据失败")]

            # 格式化预报时段
            periods = forecast_data.get("properties", {}).get("periods", [])
            if not periods:
                return [types.TextContent(type="text", text="没有可用的预报时段")]

            # 将每个时段格式化为简明字符串
            formatted_forecast = []
            for period in periods:
                forecast_text = (
                    f"{period.get('name', '未知')}:\n"
                    f"温度: {period.get('temperature', '未知')}°{period.get('temperatureUnit', 'F')}\n"
                    f"风: {period.get('windSpeed', '未知')} {period.get('windDirection', '')}\n"
                    f"{period.get('shortForecast', '无可用预报')}\n"
                    "---"
                )
                formatted_forecast.append(forecast_text)

            forecast_text = f"坐标 {latitude}, {longitude} 的预报:\n\n" + "\n".join(formatted_forecast)

            return [types.TextContent(
                type="text",
                text=forecast_text
            )]
    else:
        raise ValueError(f"未知工具: {name}")

async def main():
    # 使用标准输入/输出流运行服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# 如果你想连接到自定义客户端,这是必需的
if __name__ == "__main__":
    asyncio.run(main())