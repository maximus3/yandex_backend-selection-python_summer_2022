from database import proxy, schemas

IMPORT_BATCHES = [
    {
        'items': [
            {
                'type': 'CATEGORY',
                'name': 'Товары',
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'parentId': None,
            }
        ],
        'updateDate': '2022-02-01T12:00:00.000Z',
    },
    {
        'items': [
            {
                'type': 'CATEGORY',
                'name': 'Смартфоны',
                'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            },
            {
                'type': 'OFFER',
                'name': 'jPhone 13',
                'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'price': 79999,
            },
            {
                'type': 'OFFER',
                'name': 'Xomiа Readme 10',
                'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                'price': 59999,
            },
        ],
        'updateDate': '2022-02-02T12:00:00.000Z',
    },
    {
        'items': [
            {
                'type': 'CATEGORY',
                'name': 'Телевизоры',
                'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            },
            {
                'type': 'OFFER',
                'name': "Samson 70\" LED UHD Smart",
                'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 32999,
            },
            {
                'type': 'OFFER',
                'name': "Phyllis 50\" LED UHD Smarter",
                'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 49999,
            },
        ],
        'updateDate': '2022-02-03T12:00:00.000Z',
    },
    {
        'items': [
            {
                'type': 'OFFER',
                'name': "Goldstar 65\" LED UHD LOL Very Smart",
                'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                'price': 69999,
            }
        ],
        'updateDate': '2022-02-03T15:00:00.000Z',
    },
]

EXPECTED_TREE = {
    'type': 'CATEGORY',
    'name': 'Товары',
    'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
    'price': 58599,
    'parentId': None,
    'date': '2022-02-03T15:00:00.000Z',
    'children': [
        {
            'type': 'CATEGORY',
            'name': 'Телевизоры',
            'id': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
            'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'price': 50999,
            'date': '2022-02-03T15:00:00.000Z',
            'children': [
                {
                    'type': 'OFFER',
                    'name': "Samson 70\" LED UHD Smart",
                    'id': '98883e8f-0507-482f-bce2-2fb306cf6483',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 32999,
                    'date': '2022-02-03T12:00:00.000Z',
                    'children': None,
                },
                {
                    'type': 'OFFER',
                    'name': "Phyllis 50\" LED UHD Smarter",
                    'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 49999,
                    'date': '2022-02-03T12:00:00.000Z',
                    'children': None,
                },
                {
                    'type': 'OFFER',
                    'name': "Goldstar 65\" LED UHD LOL Very Smart",
                    'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65',
                    'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2',
                    'price': 69999,
                    'date': '2022-02-03T15:00:00.000Z',
                    'children': None,
                },
            ],
        },
        {
            'type': 'CATEGORY',
            'name': 'Смартфоны',
            'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
            'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'price': 69999,
            'date': '2022-02-02T12:00:00.000Z',
            'children': [
                {
                    'type': 'OFFER',
                    'name': 'jPhone 13',
                    'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    'price': 79999,
                    'date': '2022-02-02T12:00:00.000Z',
                    'children': None,
                },
                {
                    'type': 'OFFER',
                    'name': 'Xomiа Readme 10',
                    'id': 'b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4',
                    'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                    'price': 59999,
                    'date': '2022-02-02T12:00:00.000Z',
                    'children': None,
                },
            ],
        },
    ],
}

EXPECTED_STATISTIC = {
    'items': [
        {
            'type': 'CATEGORY',
            'name': 'Товары',
            'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'date': '2022-02-01T12:00:00.000Z',
            'parentId': None,
            'price': None,
        },
        {
            'type': 'CATEGORY',
            'name': 'Товары',
            'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'date': '2022-02-02T12:00:00.000Z',
            'parentId': None,
            'price': 69999,
        },
        {
            'type': 'CATEGORY',
            'name': 'Товары',
            'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'date': '2022-02-03T12:00:00.000Z',
            'parentId': None,
            'price': 55749,
        },
        {
            'type': 'CATEGORY',
            'name': 'Товары',
            'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
            'date': '2022-02-03T15:00:00.000Z',
            'parentId': None,
            'price': 58599,
        },
    ]
}

IMPORTS_AND_NODES_DATA = [
    (
        {
            'items': [
                {
                    'type': 'CATEGORY',
                    'name': 'Категория',
                    'id': 'id1',
                },
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 1',
                    'id': 'id11',
                    'parentId': 'id1',
                },
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 2',
                    'id': 'id12',
                    'parentId': 'id1',
                },
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'tovar',
                    'price': 100,
                    'parentId': 'id1',
                },
            ],
            'updateDate': '2022-02-01T12:00:00.000Z',
        },
        {
            'type': 'CATEGORY',
            'name': 'Категория',
            'id': 'id1',
            'price': 100,
            'parentId': None,
            'date': '2022-02-01T12:00:00.000Z',
            'children': [
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 1',
                    'id': 'id11',
                    'price': None,
                    'parentId': 'id1',
                    'date': '2022-02-01T12:00:00.000Z',
                    'children': [],
                },
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 2',
                    'id': 'id12',
                    'price': None,
                    'parentId': 'id1',
                    'date': '2022-02-01T12:00:00.000Z',
                    'children': [],
                },
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'tovar',
                    'price': 100,
                    'parentId': 'id1',
                    'date': '2022-02-01T12:00:00.000Z',
                    'children': None,
                },
            ],
        },
    ),
    (
        {
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'tovar',
                    'price': 100,
                    'parentId': 'id11',
                }
            ],
            'updateDate': '2022-02-01T13:00:00.000Z',
        },
        {
            'type': 'CATEGORY',
            'name': 'Категория',
            'id': 'id1',
            'price': 100,
            'parentId': None,
            'date': '2022-02-01T13:00:00.000Z',
            'children': [
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 1',
                    'id': 'id11',
                    'price': 100,
                    'parentId': 'id1',
                    'date': '2022-02-01T13:00:00.000Z',
                    'children': [
                        {
                            'type': 'OFFER',
                            'name': 'Товар',
                            'id': 'tovar',
                            'price': 100,
                            'parentId': 'id11',
                            'date': '2022-02-01T13:00:00.000Z',
                            'children': None,
                        }
                    ],
                },
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 2',
                    'id': 'id12',
                    'price': None,
                    'parentId': 'id1',
                    'date': '2022-02-01T12:00:00.000Z',
                    'children': [],
                },
            ],
        },
    ),
    (
        {
            'items': [
                {
                    'type': 'OFFER',
                    'name': 'Товар',
                    'id': 'tovar',
                    'price': 100,
                    'parentId': 'id12',
                }
            ],
            'updateDate': '2022-02-01T14:00:00.000Z',
        },
        {
            'type': 'CATEGORY',
            'name': 'Категория',
            'id': 'id1',
            'price': 100,
            'parentId': None,
            'date': '2022-02-01T14:00:00.000Z',
            'children': [
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 1',
                    'id': 'id11',
                    'price': None,
                    'parentId': 'id1',
                    'date': '2022-02-01T14:00:00.000Z',
                    'children': [],
                },
                {
                    'type': 'CATEGORY',
                    'name': 'Подкатегория 2',
                    'id': 'id12',
                    'price': 100,
                    'parentId': 'id1',
                    'date': '2022-02-01T14:00:00.000Z',
                    'children': [
                        {
                            'type': 'OFFER',
                            'name': 'Товар',
                            'id': 'tovar',
                            'price': 100,
                            'parentId': 'id12',
                            'date': '2022-02-01T14:00:00.000Z',
                            'children': None,
                        }
                    ],
                },
            ],
        },
    ),
]


def import_batches_proxy_data():  # pragma: no cover
    return (
        [proxy.ShopUnitProxy for _ in range(len(IMPORT_BATCHES))],
        [schemas.ShopUnitSchema for _ in range(len(IMPORT_BATCHES))],
        IMPORT_BATCHES[:],
    )


def shop_unit_proxy_data():  # pragma: no cover
    return [
        import_batches_proxy_data(),
    ]


def shop_unit_proxy_data_single():  # pragma: no cover
    return [
        (
            proxy.ShopUnitProxy,
            schemas.ShopUnitSchema,
            {
                'type': 'CATEGORY',
                'name': 'Товары',
                'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                'parentId': None,
                'date': '2022-02-03T15:00:00.000Z',
            },
        ),
        (
            proxy.ShopUnitProxy,
            schemas.ShopUnitSchema,
            {
                'type': 'OFFER',
                'name': 'jPhone 13',
                'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                'parentId': None,
                'price': 79999,
                'date': '2022-02-03T15:00:00.000Z',
            },
        ),
    ]
