import asyncio


async def heavy_data_processing(data: dict):
    """Some (fake) heavy data processing logic."""
    print(data)
    message_processed = data.get("message", data)
    return message_processed
