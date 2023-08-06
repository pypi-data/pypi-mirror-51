# Copyright (c) 2019  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pytest
from mock import patch, mock_open, ANY, Mock

from module_build_service import app
from module_build_service.manage import retire, build_module_locally
from module_build_service.models import BUILD_STATES, ModuleBuild


@pytest.mark.usefixtures("model_tests_init_data")
class TestMBSManage:

    @pytest.mark.parametrize(
        ("identifier", "is_valid"),
        (
            ("", False),
            ("spam", False),
            ("spam:bacon", True),
            ("spam:bacon:eggs", True),
            ("spam:bacon:eggs:ham", True),
            ("spam:bacon:eggs:ham:sausage", False),
        ),
    )
    def test_retire_identifier_validation(self, identifier, is_valid):
        if is_valid:
            retire(identifier)
        else:
            with pytest.raises(ValueError):
                retire(identifier)

    @pytest.mark.parametrize(
        ("overrides", "identifier", "changed_count"),
        (
            ({"name": "pickme"}, "pickme:eggs", 1),
            ({"stream": "pickme"}, "spam:pickme", 1),
            ({"version": "pickme"}, "spam:eggs:pickme", 1),
            ({"context": "pickme"}, "spam:eggs:ham:pickme", 1),
            ({}, "spam:eggs", 3),
            ({"version": "pickme"}, "spam:eggs", 3),
            ({"context": "pickme"}, "spam:eggs:ham", 3),
        ),
    )
    @patch("module_build_service.manage.prompt_bool")
    def test_retire_build(self, prompt_bool, overrides, identifier, changed_count, db_session):
        prompt_bool.return_value = True

        module_builds = db_session.query(ModuleBuild).filter_by(state=BUILD_STATES["ready"]).all()
        # Verify our assumption of the amount of ModuleBuilds in database
        assert len(module_builds) == 3

        for x, build in enumerate(module_builds):
            build.name = "spam"
            build.stream = "eggs"
            build.version = "ham"
            build.context = str(x)

        for attr, value in overrides.items():
            setattr(module_builds[0], attr, value)

        db_session.commit()

        retire(identifier)
        retired_module_builds = (
            db_session.query(ModuleBuild).filter_by(state=BUILD_STATES["garbage"]).all()
        )

        assert len(retired_module_builds) == changed_count
        for x in range(changed_count):
            assert retired_module_builds[x].id == module_builds[x].id
            assert retired_module_builds[x].state == BUILD_STATES["garbage"]

    @pytest.mark.parametrize(
        ("confirm_prompt", "confirm_arg", "confirm_expected"),
        (
            (True, False, True),
            (True, True, True),
            (False, False, False),
            (False, True, True)
        ),
    )
    @patch("module_build_service.manage.prompt_bool")
    def test_retire_build_confirm_prompt(
        self, prompt_bool, confirm_prompt, confirm_arg, confirm_expected, db_session
    ):
        prompt_bool.return_value = confirm_prompt

        module_builds = db_session.query(ModuleBuild).filter_by(state=BUILD_STATES["ready"]).all()
        # Verify our assumption of the amount of ModuleBuilds in database
        assert len(module_builds) == 3

        for x, build in enumerate(module_builds):
            build.name = "spam"
            build.stream = "eggs"

        db_session.commit()

        retire("spam:eggs", confirm_arg)
        retired_module_builds = (
            db_session.query(ModuleBuild).filter_by(state=BUILD_STATES["garbage"]).all()
        )

        expected_changed_count = 3 if confirm_expected else 0
        assert len(retired_module_builds) == expected_changed_count

    @patch("module_build_service.manage.open", create=True, new_callable=mock_open)
    @patch("module_build_service.manage.submit_module_build_from_yaml")
    @patch("module_build_service.scheduler.main")
    @patch("module_build_service.manage.conf.set_item")
    @patch("module_build_service.models.make_db_session")
    def test_build_module_locally_set_stream(
        self, make_db_session, conf_set_item, main, submit_module_build_from_yaml, patched_open
    ):
        mock_db_session = Mock()
        make_db_session.return_value.__enter__.return_value = mock_db_session

        # build_module_locally changes database uri to a local SQLite database file.
        # Restore the uri to original one in order to not impact the database
        # session in subsequent tests.
        original_db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        try:
            build_module_locally(
                yaml_file="./fake.yaml", default_streams=["platform:el8"], stream="foo")
        finally:
            app.config['SQLALCHEMY_DATABASE_URI'] = original_db_uri

        submit_module_build_from_yaml.assert_called_once_with(
            mock_db_session, ANY, ANY, {
                "default_streams": {"platform": "el8"}, "local_build": True
            },
            skiptests=False, stream="foo")
