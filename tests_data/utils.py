import json
import subprocess


async def clear_used_ids(client, used_ids):  # pragma: no cover
    for used_id in used_ids:
        await client.delete(f'delete/{used_id}')


def sort_items(node):  # pragma: no cover
    if node.get('items'):
        node['items'].sort(key=lambda x: x['date'])


def deep_sort_children(node):  # pragma: no cover
    if node.get('children'):
        node['children'].sort(key=lambda x: x['id'])

        for child in node['children']:
            deep_sort_children(child)


def print_diff(expected, response):  # pragma: no cover
    with open('expected.json', 'w', encoding='utf-8') as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write('\n')

    with open('response.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write('\n')

    subprocess.run(
        [
            'git',
            '--no-pager',
            'diff',
            '--no-index',
            'expected.json',
            'response.json',
        ]
    )

    return 'output'
