import tempfile

import pytest


@pytest.fixture(scope='function')
def tempdir(request):
    directory = tempfile.mkdtemp()

    def fin():
        shutil.rmtree(directory)

    return directory


