# -*- coding: utf-8 -*-
import pytest
import peewee

from tracboat.gitlab import model


@pytest.mark.parametrize('version', [
    '8.4',
    '8.5',
    '8.7',
    '8.13',
    '8.15',
    '8.16',
    '8.17',
    '9.0.0'
])
def test_get_model_supported(version):
    M = model.get_model(version)
    assert M
    assert M.database_proxy
    assert isinstance(M.database_proxy, peewee.Proxy)


@pytest.mark.parametrize('version', [
    '8.4.0',
    '9.0.1',
    '9.0.0.0',
    '8.7.0',
])
def test_get_model_unsupported(version):
    with pytest.raises(ImportError):
        model.get_model(version)
