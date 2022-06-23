async def clear_used_ids(client, used_ids):
    for used_id in used_ids:
        await client.delete(f'delete/{used_id}')
