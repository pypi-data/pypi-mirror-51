from mergefier.mergefier import Mergefier
from github import Github
from github import AuthenticatedUser
from github import Repository
from github import GitRef
from github import PullRequest
from github import PaginatedList
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import create_autospec
from unittest.mock import PropertyMock
import pytest

def test_check_repo_existence_good():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    assert thing.check_repo_existence('repo_name') == True

def test_check_repo_existence_bad():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    thing.g.get_repo = MagicMock(return_value=False)

    with pytest.raises(Exception) as ex:
        assert thing.check_repo_existence('repo_name') == False
    assert ex.value.__str__() == "Can't find a repo with that name."

def test_create_github_connection_bad():
    thing = Mergefier()
    mock_class = create_autospec(AuthenticatedUser, instance=True)
    type(mock_class).id = PropertyMock(side_effect=Exception('foo'))
    Github.get_user = MagicMock(return_value=mock_class)

    with pytest.raises(Exception) as e:
        thing.create_github_connection("token")
    assert e.value.__str__() == "Couldn't connect to github."

def test_create_github_connection_good():
    thing = Mergefier()
    mock_class = create_autospec(AuthenticatedUser, instance=True)
    mock_class.id = 1234
    Github.get_user = MagicMock(return_value=mock_class)

    assert thing.create_github_connection("token") == 1234

def test_pr_existence_bad():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    repo = create_autospec(Repository, instance=True)
    ex = Exception()
    ex.status = 404
    ex.message = "PR not found"
    repo.get_pull = MagicMock(side_effect=ex)

    thing.g.get_repo = MagicMock(return_value=repo)

    with pytest.raises(Exception) as ex:
        assert thing.check_pr_existence('repo_name', 1) == False
    assert str(ex.value) == "Pull Request 1 not found!"
    repo.get_pull.assert_called_once_with(1)

def test_pr_existence_good():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()
    thing.g = MagicMock()

    repo = create_autospec(Repository, instance=True)
    repo.get_pull = MagicMock()

    pr = create_autospec(PullRequest.PullRequest, instance=True)

    thing.g.get_repo = MagicMock(return_value=repo)
    repo.get_pull = MagicMock(return_value=pr)

    assert thing.check_pr_existence('repo_name', 1) == pr
    repo.get_pull.assert_called_once_with(1)

def test_pr_mergeability_good():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository, instance=True)
    pr = create_autospec(PullRequest.PullRequest, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)
    repo.get_pull = MagicMock(return_value=pr)

    pr.mergeable = True

    assert thing.check_pr_mergeability(pr) == True

def test_pr_mergeability_bad():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository, instance=True)
    pr = create_autospec(PullRequest.PullRequest, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)
    repo.get_pull = MagicMock(return_value=pr)

    pr.mergeable = False

    with pytest.raises(Exception) as ex:
        assert thing.check_pr_mergeability(pr) == False
    assert str(ex.value) == "PR is not mergeable!"

def test_merge_pr_good():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository.Repository, instance=True)
    pr = create_autospec(PullRequest.PullRequest, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)
    repo.get_pull = MagicMock(return_value=pr)

    assert thing.merge_pr("repo_name", pr) == True
    pr.merge.assert_called_once_with()

def test_merge_pr_bad():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository.Repository, instance=True)
    pr = create_autospec(PullRequest.PullRequest, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)
    repo.get_pull = MagicMock(return_value=pr)

    e = Exception("Problem merging pull request.")
    pr.merge = MagicMock(side_effect=e)

    with pytest.raises(Exception) as ex:
        assert thing.merge_pr("repo_name", pr) == False
    assert str(ex.value) == "Problems merging pull request."
    pr.merge.assert_called_once_with()

def test_delete_branch_good():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository.Repository, instance=True)
    pr = create_autospec(PullRequest.PullRequest, instance=True)
    branch = create_autospec(GitRef.GitRef, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)
    repo.get_pull = MagicMock(return_value=pr)
    repo.get_git_ref = MagicMock(return_value=branch)

    pr.head.ref = 'hotfix-branch'

    assert thing.delete_branch("repo_name", pr) == True
    branch.delete.assert_called_once_with()

def test_delete_branch_bad():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository.Repository, instance=True)
    pr = create_autospec(PullRequest.PullRequest, instance=True)
    branch = create_autospec(GitRef.GitRef, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)
    repo.get_pull = MagicMock(return_value=pr)
    repo.get_git_ref = MagicMock(return_value=branch)

    pr.head.ref = 'hotfix-branch'

    branch.delete = MagicMock(side_effect=Exception("Problem deleting branch."))

    with pytest.raises(Exception) as ex:
        assert thing.delete_branch("repo_name", pr) == False
    assert str(ex.value) == "Problems deleting branch"
    branch.delete.assert_called_once_with()

def test_tag_master_good():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository.Repository, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)

    assert thing.tag_master("repo_name", 'commit_sha') == True
    repo.create_git_ref.assert_called_once_with('refs/tags/latest','commit_sha')

def test_tag_master_bad():
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    repo = create_autospec(Repository.Repository, instance=True)

    thing.g = github_connection
    github_connection.get_repo = MagicMock(return_value=repo)
    repo.create_git_ref = MagicMock(side_effect=Exception("Problem creating ref."))

    with pytest.raises(Exception) as ex:
        assert thing.tag_master("repo_name", 'commit_sha') == False
    assert str(ex.value) == "Problems creating tag"
    repo.create_git_ref.assert_called_once_with('refs/tags/latest','commit_sha')

def test_get_current_commit_good():
    thing = Mergefier()
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
    thing = Mergefier()
    thing.create_github_connection = MagicMock()

    github_connection = create_autospec(Github)
    thing.g = github_connection

    repo = create_autospec(Repository.Repository, instance=True)
    github_connection.get_repo = MagicMock(return_value=repo)

    repo.get_commits = MagicMock(side_effect=Exception("Can't get commits"))
    # thing.run_checks = MagicMock(return_value=True)
    assert thing.get_current_commit("repo_name") == False
    repo.get_commits.assert_called_once_with()
