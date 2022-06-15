import pytest
from sqlalchemy.exc import InvalidRequestError

from database.proxy import ShopUnitProxy
from tests.static import shop_unit_proxy_data_single


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_eq_error(
    prepare_db_shop_unit_single_env, model, model_schema, parameters
):
    assert not model.get(**parameters) == 1


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_create_error_no_such_param(
    prepare_db_env, model, model_schema, parameters
):
    with pytest.raises(TypeError):
        model.create(**parameters, no_param='no_param')


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_create(prepare_db_env, model, model_schema, parameters):
    model.create(**parameters)
    assert model.get(**parameters) is not None


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_create_session_is_not_none(
    prepare_db_env, create_session, model, model_schema, parameters
):
    with create_session() as session:
        assert model.create(session, **parameters) is False
        assert model.get(session, **parameters) is None


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_or_create(prepare_db_env, model, model_schema, parameters):
    assert model.get_or_create(**parameters) is not None
    assert model.get(**parameters) is not None


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_or_create_session_is_not_none(
    prepare_db_env, create_session, model, model_schema, parameters
):
    with create_session() as session:
        assert model.get_or_create(session, **parameters) is None
        assert model.get(session, **parameters) is None


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_or_create_error_no_such_param(
    prepare_db_env, model, model_schema, parameters
):
    with pytest.raises(InvalidRequestError):
        model.get_or_create(**parameters, no_param='no_param')


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_or_create_exists(
    prepare_db_shop_unit_single_env, model, model_schema, parameters
):
    assert model.get_or_create(**parameters) is not None


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_none(prepare_db_env, model, model_schema, parameters):
    assert model.get(**parameters) is None


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_expect(
    prepare_db_shop_unit_single_env, model, model_schema, parameters
):
    assert model.get_expect(**parameters)


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_model(
    prepare_db_shop_unit_single_env,
    create_session,
    model,
    model_schema,
    parameters,
):
    assert model.get_model(**parameters)
    with create_session() as session:
        assert model(
            model.get_model(**parameters, session=session)
        ) == model.get_expect(**parameters)


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_schema_model(
    prepare_db_shop_unit_single_env,
    create_session,
    model,
    model_schema,
    parameters,
):
    assert model.get_schema_model(**parameters)
    with create_session() as session:
        assert model.get_schema_model(**parameters) == model_schema.from_orm(
            model.get_model(**parameters, session=session)
        )


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_get_all(
    prepare_db_shop_unit_single_env, model, model_schema, parameters
):
    assert model.get_all(**parameters) == [model.get_expect(**parameters)]


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_update_none(
    prepare_db_shop_unit_single_env, model, model_schema, parameters
):
    proxy_model = model.get(**parameters)
    proxy_model.uuid = -1
    assert not proxy_model.update(**parameters)


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_update_no_attr(
    prepare_db_shop_unit_single_env, model, model_schema, parameters
):
    proxy_model = model.get(**parameters)
    parameters['no_such_parameter'] = 'no_such_parameter'
    assert not proxy_model.update(**parameters)


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_update(
    prepare_db_shop_unit_single_env, model, model_schema, parameters
):
    assert model.get(**parameters).update(**parameters)
    assert model.get(**parameters) is not None


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_update_session_is_not_none(
    prepare_db_shop_unit_single_env,
    create_session,
    model,
    model_schema,
    parameters,
):
    with create_session() as session:
        assert model.get(**parameters).update(session, **parameters) is False


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_delete_session_is_not_none(
    prepare_db_shop_unit_single_env,
    create_session,
    model,
    model_schema,
    parameters,
):
    with create_session() as session:
        assert model.get(**parameters).delete(session) is False


@pytest.mark.parametrize(
    ('model', 'model_schema', 'parameters'),
    shop_unit_proxy_data_single(),
)
def test_proxy_delete_session(
    prepare_db_shop_unit_single_env,
    create_session,
    model,
    model_schema,
    parameters,
):
    assert model.get(**parameters).delete() is True
    assert model.get(**parameters) is None


def test_can_not_call_private_methods_without_session(
    prepare_db_shop_unit_single_env,
):
    with pytest.raises(ValueError):
        ShopUnitProxy.get_all()[0]._delete(None)

    with pytest.raises(ValueError):
        ShopUnitProxy.get_all()[0]._update(None)

    with pytest.raises(ValueError):
        ShopUnitProxy._create(None)
