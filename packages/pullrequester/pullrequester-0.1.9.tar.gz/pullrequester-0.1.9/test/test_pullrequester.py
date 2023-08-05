from pullrequester.pullrequester import PullRequester
from github import Github
from github import AuthenticatedUser
from github import Repository
from github import PaginatedList
from github import Issue
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import create_autospec
from unittest.mock import PropertyMock
import pytest

def test_check_repo_existence_good():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    assert thing.check_repo_existence('repo_name') == True

def test_check_repo_existence_bad():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    thing.g.get_repo = MagicMock(return_value=False)

    with pytest.raises(Exception) as ex:
        assert thing.check_repo_existence('repo_name') == False
    assert ex.value.__str__() == "'bool' object has no attribute 'id'"

def test_create_github_connection_bad():
    thing = PullRequester()
    mock_class = create_autospec(AuthenticatedUser, instance=True)
    type(mock_class).id = PropertyMock(side_effect=Exception("Couldn't connect to github."))
    Github.get_user = MagicMock(return_value=mock_class)

    with pytest.raises(Exception) as e:
        thing.create_github_connection("token")
    assert e.value.__str__() == "Couldn't connect to github."

def test_create_github_connection_good():
    thing = PullRequester()
    mock_class = create_autospec(AuthenticatedUser, instance=True)
    mock_class.id = 1234
    Github.get_user = MagicMock(return_value=mock_class)

    assert thing.create_github_connection("token") == 1234

def test_check_branch_existence_bad():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    repo = create_autospec(Repository, instance=True)
    ex = Exception()
    ex.status = 404
    ex.message = "Branch branch_name not found!"
    repo.get_branch = MagicMock(side_effect=ex)

    thing.g.get_repo = MagicMock(return_value=repo)

    with pytest.raises(Exception) as e:
        assert thing.check_branch_existence('repo_name', 'branch_name') == False
    assert e.value.message == "Branch branch_name not found!"
    repo.get_branch.assert_called_once_with('branch_name')

def test_check_branch_existence_good():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    repo = create_autospec(Repository, instance=True)
    repo.get_branch = MagicMock()

    thing.g.get_repo = MagicMock(return_value=repo)

    assert thing.check_branch_existence('repo_name', 'branch_name') == True
    repo.get_branch.assert_called_once_with('branch_name')


def test_create_issue_good():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    issue = create_autospec(Issue.Issue, instance=True)
    repo.create_issue = MagicMock(return_value=issue)

    # thing.run_checks = MagicMock(return_value=True)
    assert thing.create_issue("repo_name","branch_name_origin", "branch_name_destination") == issue
    repo.create_issue.assert_called_once_with("Pull Request from branch branch_name_origin to branch branch_name_destination")

def test_create_issue_bad():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    repo.create_issue = MagicMock(side_effect=Exception("Problem creating issue."))
    # thing.run_checks = MagicMock(return_value=True)
    with pytest.raises(Exception) as ex:
        assert thing.create_issue("repo_name","branch_name_origin", "branch_name_destination") == False
    repo.create_issue.assert_called_once_with("Pull Request from branch branch_name_origin to branch branch_name_destination")

def test_create_pr_good():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    issue = create_autospec(Issue.Issue, instance=True)

    # thing.run_checks = MagicMock(return_value=True)
    assert thing.create_pr("repo_name","branch_name_origin", "branch_name_destination", issue) == True
    repo.create_pull.assert_called_once_with(issue=issue, base="branch_name_destination", head="branch_name_origin")

def test_create_pr_bad():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    issue = create_autospec(Issue.Issue, instance=True)

    repo.create_pull = MagicMock(side_effect=Exception("Problem creating pull request."))
    # thing.run_checks = MagicMock(return_value=True)
    with pytest.raises(Exception) as ex:
        assert thing.create_pr("repo_name","branch_name_origin", "branch_name_destination", issue) == False
    repo.create_pull.assert_called_once_with(issue=issue, base="branch_name_destination", head="branch_name_origin")

def test_list_branches_good():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    branches = []

    repo.get_branches = MagicMock(return_value=branches)

    # thing.run_checks = MagicMock(return_value=True)
    assert thing.list_branches("repo_name") == branches
    repo.get_branches.assert_called_once_with()

def test_list_branches_bad():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    repo.get_branches = MagicMock(side_effect=Exception("Problem creating pull request."))

    with pytest.raises(Exception) as ex:
        assert thing.list_branches("repo_name")
    repo.get_branches.assert_called_once_with()

def test_get_current_commit_good():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    commits = create_autospec(PaginatedList.PaginatedList)
    repo.get_commits = MagicMock(return_value=commits)

    commits[0].sha = 'commit_sha'

    # thing.run_checks = MagicMock(return_value=True)
    assert thing.get_current_commit("repo_name") == 'commit_sha'
    repo.get_commits.assert_called_once_with()

def test_get_current_commit_bad():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    repo.get_commits = MagicMock(side_effect=Exception("Can't get commits"))
    # thing.run_checks = MagicMock(return_value=True)
    with pytest.raises(Exception) as ex:
        assert thing.get_current_commit("repo_name") == False
    repo.get_commits.assert_called_once_with()

def test_delete_prs_good():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    assert thing.delete_prs("repo_name") == True
    repo.get_pulls.assert_called_once_with(state='open')

def test_delete_prs_bad():
    thing = PullRequester()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    repo.get_pulls = MagicMock(side_effect=Exception("Can't get pulls"))
    # thing.run_checks = MagicMock(return_value=True)
    with pytest.raises(Exception) as ex:
        assert thing.delete_prs("repo_name") == False
    repo.get_pulls.assert_called_once_with(state='open')
    assert ex.value.__str__() == "Can't get pulls"
