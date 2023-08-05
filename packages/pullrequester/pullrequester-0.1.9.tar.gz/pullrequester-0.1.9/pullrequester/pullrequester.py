#!/usr/bin/env python3
import sys
from github import Github
from gitator import Gitator
import re


class PullRequester:

    def request_pull(self, github_token, repo_name, branch_name):
        print("Entering method requestpull(**********, " + repo_name + "," + branch_name + ")")
        gitator = Gitator()
        gitator.create_github_connection(github_token)

        gitator.check_repo_existence(repo_name)

        if branch_name == 'merge_back':
            branch_list = gitator.list_branches(repo_name)
            gitator.delete_prs(repo_name)

            branch_name_origin = 'master'
            for branch in branch_list:
                branch_name_destination = branch.name
                i = gitator.create_issue(repo_name, branch_name_origin, branch_name_destination)
                gitator.create_pr(repo_name, branch_name_origin, branch_name_destination, i)
        else:
            branch_name_origin = branch_name
            branch_name_destination = 'master'
            if not gitator.check_branch_existence(repo_name, branch_name_origin):
                raise Exception('Branch not found.')
            i = gitator.create_issue(repo_name, branch_name_origin, branch_name_destination)
            gitator.create_pr(repo_name, branch_name_origin, branch_name_destination, i)

    def check_input(self):
        if len(sys.argv) < 4:
            raise Exception("Usage: " + sys.argv[0] + " <github_token> <repo_name> <branch_name>")
