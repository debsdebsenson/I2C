import pytest

from appI2C.session.session_menu import SessionMenuRegular # type: ignore

#parametrize = pytest.mark.parametrize

class TestSessionMenuRegular:
    #def test_edit_session(self, capsys):
    def test_this_is_for_testing_initially(self):
        with pytest.raises(SystemExit):
            SessionMenuRegular.this_is_for_testing_initially()
        #self.value=1
        #SessionMenuRegular.edit_session()
        #assert self.value == y
        #out,err=capsys.readouterr()
        #assert out=="Editing sessions will be implemented in the future"