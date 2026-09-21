from python_a2a.mcp import FastMCP

HOST = "127.0.0.1"
PORT = 6005

mcp = FastMCP(
    name="WeatherTool",
    description="Weather lookup tools.",
)


@mcp.tool(name="get_weather", description="Look up the weather for a city.")
def get_weather(city: str) -> str:
    print(f"[MCP weather tool] city={city}")
    city_key = city.strip().lower()
    if city_key == "beijing":
        return "Beijing is sunny today, 29°C."
    if city_key == "shanghai":
        return "Shanghai is cloudy today, 24°C."
    return f"No weather data for {city}."


if __name__ == "__main__":
    print(f"[MCP weather tool] listening on http://{HOST}:{PORT}")
    mcp.run(transport="fastapi", host=HOST, port=PORT)
