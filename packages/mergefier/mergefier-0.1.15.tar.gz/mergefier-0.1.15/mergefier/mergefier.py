#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# from github import Github
from gitator import Gitator
from slackclient import SlackClient


class Mergefier:

    def mergefy(self, github_token, repo_name, pr_id, slack_token):
        print("Entering method mergefy(**********, " + repo_name + "," + pr_id + ")")
        gitator = Gitator()
        gitator.create_github_connection(github_token)

        gitator.check_repo_existence(repo_name)

        if pr_id == 'merge_back':
            # List PRs
            prs = gitator.list_prs(repo_name)
            # For each pr
            for pr in prs:
                print(pr)
                # check if pr is merge back
                if (pr.base.ref != 'master' and pr.head.ref == 'master'):
                    # check_pr_mergeability
                    try:
                        gitator.check_pr_mergeability(pr)
                        # merge_pr
                        gitator.merge_pr(repo_name, pr)
                        sc = SlackClient(slack_token)
                        sc.api_call('chat.postMessage',
                                    channel='#merge_back',
                                    attachments=[{
                                        "color": "#00FF00",
                                        "title": "Merge Back Com Sucesso",
                                        "fallback": "Merge Back Com Sucesso",
                                        "title_link": pr.html_url,
                                        "text": 'Pessoal, fiz um merge back com sucesso. Fiquem atentos às mudanças de código nas branches',
                                        "fields": [
                                            {
                                                "title": "Repo",
                                                "value": "<" + pr.base.repo.html_url + "|" + repo_name + ">"
                                            },
                                            {
                                                "title": "Branch",
                                                "value": pr.base.ref
                                            },
                                            {
                                                "title": "PR",
                                                "value": "<" + pr.html_url + "|" + pr.title + " (#" + str(pr.number) + ")>"
                                            }
                                        ]
                                    }])
                    except Exception as ex:
                        # can't merge? exception handling
                        sc = SlackClient(slack_token)
                        sc.api_call('chat.postMessage',
                                    channel='#merge_back',
                                    attachments=[{
                                        "color": "#FF0000",
                                        "title": "Merge Back FALHOU",
                                        "fallback": "Merge Back FALHOU",
                                        "title_link": pr.html_url,
                                        "text": 'Pessoal, não consegui fazer o merge de uma PR. O dono da branch tem que analisar se existem conflitos a serem resolvidos e solicitar o merge novamente.',
                                        "fields": [
                                            {
                                                "title": "Repo",
                                                "value": "<" + pr.base.repo.html_url + "|" + repo_name + ">"
                                            },
                                            {
                                                "title": "Branch",
                                                "value": pr.base.ref
                                            },
                                            {
                                                "title": "PR",
                                                "value": "<" + pr.html_url + "|" + pr.title + " (#" + str(pr.number) + ")>"
                                            },
                                            {
                                                "title": "Error Message",
                                                "value": str(ex)
                                            }
                                        ]
                                    }])

                        print("Can't merge this one. Slack message sent.")
                        print(ex)
        else:
            pr = gitator.check_pr_existence(repo_name, pr_id)
            gitator.check_pr_mergeability(pr)

            gitator.merge_pr(repo_name, pr)
            gitator.delete_branch(repo_name, pr)

            commit_sha = gitator.get_current_commit(repo_name)
            gitator.tag_master(repo_name, commit_sha)

    def check_input(self):
        if len(sys.argv) < 5:
            raise Exception("Usage: " + sys.argv[0] + " <github_token> <repo_name> <pull_request_id> <slack_token>")
