#!/usr/bin/env python3
"""
Automatically tags branches base on commit message
"""
import logging

import semantic_version
from git import Repo


# Types of changes
MAJOR = 100
MINOR = 10
PATCH = 1
CHANGE_TYPES = {
    MAJOR: 'MAJOR',
    MINOR: 'MINOR',
    PATCH: 'PATCH',
}


PREFIX_TO_ELIMINATE = ['v']


class AutoTag():
    """Class  wrapper for auto-tag functionality."""

    def __init__(self, repo, branch, upstream_remotes, logger=None):
        """Initializa the AutoTag class.

        :param logger: If an existing logger is to be used
        :param args: CLI arguments
        """
        self._logger = logger or logging.getLogger(__name__)
        self._repo = repo
        self._branch = branch
        self._upstream_remotes = upstream_remotes or []

    def _clean_tag_name(self, tag_name):
        """Remove common mistakes when using semantic versioning."""
        for prefix in PREFIX_TO_ELIMINATE:
            if tag_name.startswith(prefix):
                clean_tag = tag_name[len(prefix):]
                self._logger.debug(
                    'Cleaning tag %s -> %s', tag_name, clean_tag)
                return clean_tag
        return tag_name

    def get_latest_tag(self, repo):
        """Return the last tag for the given repo in a Version class.
        :param repo: Repository to query for tags
        :type repo: git.Repo

        :returns: The latest tag from the repository
        :rtype: semantic_version.Version
        """
        latest_tag = None
        tags_name = [self._clean_tag_name(tag.name) for tag in repo.tags]
        sem_versions = [
            semantic_version.Version(tag_name) for tag_name in tags_name
        ]
        if sem_versions:
            latest_tag = max(sem_versions)
        self._logger.debug('Found latest tag %s', latest_tag)
        return latest_tag

    @staticmethod
    def bump_tag(tag, change_type):
        """Return the next tag version based on the change type."""
        if tag is None:
            return semantic_version.Version('0.0.1')

        if change_type == MAJOR:
            return tag.next_major()

        if change_type == MINOR:
            return tag.next_minor()

        return tag.next_patch()

    def get_all_commits_from_a_tag(self, repo, branch, tag):
        """
        Return all commits from the branch that
        happened father the specified tag.

        :param repo: Repository to query for commits
        :type repo: git.Repo

        :param branch: Branch to work on
        :type branch: str

        :param repo: Tag to stop the query at.
        :type repo: semantic_version.Version

        :returns: List of commits.
        :rtype: list of git.Commit
        """
        stop_commit = None
        if str(tag) in repo.tags:
            stop_commit = repo.tags[str(tag)].commit

        commits = []
        for commit in repo.iter_commits(rev=branch):
            if commit == stop_commit:
                break
            commits.append(commit)
        self._logger.debug(
            'Commits found from after tag %s: %s', tag, commits)
        return commits

    def get_change_type(self, commits):
        """Based on the commit message decide the change type.
        Change types can be PATCH, MINOR, MAJOR.

        Everything by default is a PATCH

        If the message stars with `fix` -> it remains a PATCH
        If the message starts with `feat` -> it becomes a MINOR

        If the message contains `BREAKING_CHANGE` -> it becomes a MAJOR

            :Example:

            ```
            fix(msk): fix logging bug
            ```
            This is a PATCH

            ```
            feature(rds): add multi AZ support
            ```
            This is a MINOR

            ```
            fix(msk): fix logging bug
            BREAKING_CHANGE: Introduce mandatory configuration
            ```
            This is a MAJOR

            ```
            feature(rds): add multi AZ support

            BREAKING_CHANGE: Requires downtime
            ```
            This is a MAJOR

        :param commits: List of commits
        :type: list of git.Commit

        :return: Type of change (PATCH, MINOR, MAJOR). By default everything
                 is a PATCH
        :rtype: int (constants)
        """
        change_type = PATCH
        for commit in commits:
            if commit.message.strip().startswith('feature('):
                change_type = max(change_type, MINOR)

            if 'BREAKING_CHANGE' in commit.message.upper():
                change_type = max(change_type, MAJOR)
            self._logger.debug(
                'Commit %s enforced %s change type', commit,
                CHANGE_TYPES[change_type])
        return change_type

    @staticmethod
    def get_remote(repo, name):
        """Return the git.Remote object base on the name."""
        for remote in repo.remotes:
            if remote.name == name:
                return remote
        return None

    def push_to_remotes(self, repo, tag):
        """Push a tag to the specified remotes."""
        if self._upstream_remotes:
            self._logger.info('Start pushing to remotes.')
        else:
            self._logger.info('No push remote was specified')
        for remote_name in self._upstream_remotes:
            remote = self.get_remote(repo, remote_name)
            if remote:
                self._logger.info('Push %s to %s', tag, remote)
                remote.push(str(tag))
            else:
                self._logger.error(
                    'Can\'t find remote with name `%s`', remote_name)

    def work(self):
        """Main entry point.

        :param args: Argument to work on
        """
        repo = Repo(self._repo)
        self._logger.info('Start tagging %s', repo)
        last_tag = self.get_latest_tag(repo)

        self._logger.info('Found tag %s', last_tag)
        commits = self.get_all_commits_from_a_tag(
            repo, self._branch, last_tag)
        type_of_change = self.get_change_type(commits)
        next_tag = self.bump_tag(last_tag, type_of_change)

        self._logger.info('Bumping tag %s -> %s', last_tag, next_tag)
        repo.create_tag(str(next_tag))

        self.push_to_remotes(repo, next_tag)
