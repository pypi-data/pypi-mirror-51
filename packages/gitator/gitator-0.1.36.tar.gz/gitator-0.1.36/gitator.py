#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from github import Github
import re


class Gitator:

    def create_github_connection(self, github_token):
        print("Entering method create_github_connection()")
        self.g = Github(github_token)
        u = self.g.get_user()

        return u.id

    def add_team_to_repo(self, repo_name, team):
        print("Entering method add_team_to_repo(" + repo_name + ", " + str(team) + ")")
        r = self.g.get_repo(repo_name)
        org_name = repo_name.split('/')[0]
        o = self.g.get_organization(org_name)

        for t in o.get_teams():
            if t.slug == team:
                t.add_to_repos(r)
                t.set_repo_permission(r, 'push')
        return True

    def replace_repo_teams(self, repo_name, teams):
        print("Entering method replace_repo_teams(" + repo_name + ", " + str(teams) + ")")
        r = self.g.get_repo(repo_name)

        for t in r.get_teams():
            if (t.slug not in teams):
                t.remove_from_repos(r)

        org_name = repo_name.split('/')[0]
        o = self.g.get_organization(org_name)

        for t in o.get_teams():
            if t.slug in teams:
                t.add_to_repos(r)
                t.set_repo_permission(r, 'push')
        return True

    # def protect_branch(self, repo_name, branch_name, status_name, teams):
    #     print("Entering method protect_branch("+repo_name+", "+branch_name+", "+str(status_name)+", "+str(teams)+")")
    #     r=self.g.get_repo(repo_name)
    #     r.protect_branch('master',True,True,status_name,True,{"users":[],"teams":teams})
    #     return True

    def check_repo_existence(self, repo_name):
        print("Entering method check_repo_existence(" + repo_name + ")")
        r = self.g.get_repo(repo_name)

        r.id
        return True

    def check_pr_existence(self, repo_name, pr_id):
        print("Entering method check_pr_existence(" + repo_name + "," + str(pr_id) + ")")

        r = self.g.get_repo(repo_name)
        pr = r.get_pull(int(pr_id))
        return pr

    def check_pr_mergeability(self, pr):
        print("Entering method check_pr_mergeability(" + str(pr) + ")")
        status = pr.mergeable
        if (status is False):
            raise Exception("PR is not mergeable!")
        return status

    def list_forks(self, repo_name):
        print("Entering method list_forks(" + str(repo_name) + ")")
        r = self.g.get_repo(repo_name)

        if r.forks == 0:
            message = "O repositório " + repo_name + " não possui nenhum fork."
        else:
            message = "O repositório " + repo_name + " possui " + str(r.forks) + " forks. Segue lista abaixo:"
            for fork in r.get_forks():
                message += "\n" + fork.full_name
        return message

    def list_repos(self, org_name):
        print("Entering method list_repos(" + str(org_name) + ")")
        o = self.g.get_organization(org_name)
        return o.get_repos()

    def merge_pr(self, repo_name, pr):
        print("Entering method merge_pr(" + repo_name + "," + str(pr) + ")")
        # r = self.g.get_repo(repo_name)

        pr.merge()
        return True

    def create_pr(self, repo_name, branch_name_origin, branch_name_destination, issue):
        print("Entering method create_pr(" + repo_name + "," + branch_name_origin + ", " + branch_name_destination + ", " + issue.__str__() + ")")
        r = self.g.get_repo(repo_name)

        try:
            r.create_pull(issue=issue, base=branch_name_destination, head=branch_name_origin)
        except Exception as ex:
            if re.match('No commits between', ex.data['errors'][0]['message']):
                print(ex.data['errors'][0]['message'])
            else:
                raise ex
            return False
        else:
            print("Pull request created successfully.")
            return True

    def delete_prs(self, repo_name):
        print("Entering method delete_prs(" + repo_name + ")")
        r = self.g.get_repo(repo_name)

        prs = r.get_pulls(state='open')

        for pr in prs:
            if (pr.base.ref != 'master' and pr.head.ref == 'master'):
                pr.edit(state='closed')
        return True

    def check_branch_existence(self, repo_name, branch_name):
        print("Entering method check_branch_existence(" + repo_name + "," + branch_name + ")")
        r = self.g.get_repo(repo_name)

        try:
            r.get_branch(branch_name)
            return True
        except Exception as ex:
            if ex.status == 404:
                return False
            else:
                raise ex

    def create_branch(self, repo_name, branch_name, commit_sha):
        print("Entering method create_branch(" + repo_name + "," + branch_name + "," + commit_sha + ")")
        r = self.g.get_repo(repo_name)

        r.create_git_ref("refs/heads/" + branch_name, commit_sha)
        return True

    def delete_branch(self, repo_name, pr):
        print("Entering method delete_branch(" + repo_name + "," + str(pr) + ")")
        r = self.g.get_repo(repo_name)

        branch_ref = pr.head.ref
        if (branch_ref == 'master'):
            raise Exception("You tried to delete the master branch. Bad python.")
        print("Deleting branch: " + branch_ref)
        b = r.get_git_ref('heads/' + branch_ref)
        b.delete()
        return True

    def list_branches(self, repo_name):
        print("Entering method list_branches(" + repo_name + ")")
        r = self.g.get_repo(repo_name)

        branch_list = []
        branches = r.get_branches()
        for branch in branches:
            if branch.name != 'master':
                branch_list.append(branch)
        return branch_list

    def get_current_commit(self, repo_name):
        print("Entering method get_current_commit(" + repo_name + ")")

        r = self.g.get_repo(repo_name)
        return r.get_commits()[0].sha

    def create_issue(self, repo_name, branch_name_origin, branch_name_destination):
        print("Entering method create_issue(" + repo_name + ", " + branch_name_origin + ", " + branch_name_destination + ")")
        r = self.g.get_repo(repo_name)

        title = "Pull Request from branch " + branch_name_origin + " to branch " + branch_name_destination

        i = r.create_issue(title)
        print("Issue created successfully.")
        return i

    def list_prs(self, repo_name):
        print("Entering method list_prs(" + repo_name + ")")
        r = self.g.get_repo(repo_name)

        return r.get_pulls()

    def tag_master(self, repo_name, commit_sha):
        print("Entering method tag_master("+ repo_name + ", " + commit_sha + ")")
        r = self.g.get_repo(repo_name)
        try:
            r.get_git_ref('tags/latest').delete()
        except:
            pass

        r.create_git_ref('refs/tags/latest', commit_sha)
        return True
