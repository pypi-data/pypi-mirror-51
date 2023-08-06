# Copyright 2019 RStudio, Inc.
# All rights reserved.
#
# Use of this source code is governed by a BSD 2-Clause
# license that can be found in the LICENSE_BSD file.

from urllib.parse import urlparse
from dateutil.parser import parse as dateparse

from buildbot.util.logger import Logger
from buildbot.www.hooks.github import GitHubEventHandler
from buildbot.process.properties import Properties

from .utils import ensure_deferred, GithubClientService
from .commands import CommandError

__all__ = ['GithubHook', 'UrsabotHook']

log = Logger()


class GithubHook(GitHubEventHandler):
    """Converts github events to changes

    It extends the original implementation for push and pull request events
    with a pull request comment event in order to drive buildbot with github
    comments.

    Github hook creates 4 kinds of changes, distinguishable by their category
    field:

    None: This change is a push to a branch.
        Use ursabot.changes.ChangeFilter(
            category=None,
            repository="http://github.com/<org>/<project>"
        )
    'tag': This change is a push to a tag.
        Use ursabot.changes.ChangeFilter(
            category='tag',
            repository="http://github.com/<org>/<project>"
        )
    'pull': This change is from a pull-request creation or update.
        Use ursabot.changes.ChangeFilter(
            category='pull',
            repository="http://github.com/<org>/<project>"
        )
        In this case, the GitHub step must be used instead of the standard Git
        in order to be able to pull GitHub’s magic refs (refs/pull/<id>/merge).
        With this method, the GitHub step will always checkout the branch
        merged with latest master. This allows to test the result of the merge
        instead of just the source branch.
        Note that you can use the GitHub for all categories of event.
    'comment': This change is from a pull-request comment requested by a
        comment like: `@ursabot <command>`. Two special properties will be set
        `event: issue_comment` and `command: <command>`.
        Use ursabot.changes.ChangeFilter(
            category='comment',
            repository="http://github.com/<org>/<project>"
        )
        Optionally filter with properties: ursabot.changes.ChangeFilter(
            category='comment',
            repository="http://github.com/<org>/<project>",
            properties={
                'event': 'issue_comment',
                'command': '<command>'
            }
        )
    """

    # there is no easy way to pass additional arguments for this object,
    # so configure and store them as class attributes
    botname = 'buildbot'
    headers = {'User-Agent': 'Buildbot'}
    use_reactions = False

    # comment_handler is a callback which receives a comment as plain
    # string and should raise a commands.CommandError on parse failure
    # otherwise should return a dictionary of properties
    comment_handler = None

    def __init__(self, *args, tokens=None, token=None,
                 github_property_whitelist=None, **kwargs):
        # only `token` argument is passed to the event handler, a plugin is
        # required to cleanly load other hook handlers with custom arguments
        if tokens is None:
            if token is None:
                self._tokens = []
            elif isinstance(token, (list, tuple)):
                self._tokens = token
            else:
                self._tokens = [token]
        elif isinstance(tokens, (list, tuple)):
            self._tokens = tokens
        else:
            raise ValueError('token(s) argument must be a list or tuple')

        if not github_property_whitelist:
            # handle_pull_request calls self.extractProperties with
            # payload['pull_request'], so in order to set a title property
            # to the pull_request's title, 'github.title' must be passed to
            # the property whitelist, for the exact implementation see
            # buildbot.changes.github.PullRequestMixin and handle_pull_request
            kwargs['github_property_whitelist'] = ['github.title']

        # the http client service is initialized on the first use
        self._http = None

        super().__init__(*args, **kwargs)

    def _as_hook_dialect_config(self):
        # the change hooks can be configured in a bit twisted fashion
        # return the dictionary required to configure this object through
        # the buildmaster config
        hook_arguments = {
            'class': self.__class__,
            'secret': self._secret,
            'token': self._tokens,
            'debug': self.debug,
            'strict': self._strict,
            'verify': self.verify,
            'codebase': self._codebase,
            'pullrequest_ref': self.pullrequest_ref,
            'github_api_endpoint': self.github_api_endpoint,
            'github_property_whitelist': self.github_property_whitelist,
            'skips': self.skips
        }
        return {'github': hook_arguments}

    async def _client(self):
        # return if the service has been already initialized
        if self._http:
            return self._http

        # render the secrets passed to tokens
        props = Properties()
        props.master = self.master
        tokens = [await props.render(token) for token in self._tokens]

        self._http = await GithubClientService.getService(
            self.master,
            self.github_api_endpoint,
            tokens=tokens,
            headers=self.headers,
            debug=self.debug,
            verify=self.verify
        )
        return self._http

    async def _get(self, url, headers=None):
        url = urlparse(url)
        client = await self._client()
        response = await client.get(url.path, headers=headers)
        result = await response.json()
        return result

    async def _post(self, url, data, headers=None):
        url = urlparse(url)
        client = await self._client()
        response = await client.post(url.path, json=data, headers=headers)
        result = await response.json()
        log.info(f'POST to {url} with the following result: {result}')
        return result

    async def _get_commit_msg(self, repo, sha):
        """Queries the commit message from the API

        Used by handle_pull_request.

        License note:
           Copied from the original buildbot implementation with minor
           modifications.
        """
        url = f'/repos/{repo}/commits/{sha}'
        result = await self._get(url)
        commit = result.get('commit', {})
        return commit.get('message', 'No message field')

    async def _get_pull_request_files(self, repo, number):
        """Queries the files affected by a pull request

        Returns the affected files, no matter whether the file was added,
        removed or changed.
        """
        url = f'/repos/{repo}/pulls/{number}/files'
        result = await self._get(url) or []
        return [file['filename'] for file in result]

    @ensure_deferred
    async def handle_pull_request(self, payload, event, allow_skip=True):
        """Handles the pull request event

        Also queries the commit's message and the files affected by the pull
        request.

        License note:
           Copied from the original buildbot implementation with minor
           modifications and additions.
        """
        changes = []
        number = payload['number']
        refname = f'refs/pull/{number}/{self.pullrequest_ref}'
        basename = payload['pull_request']['base']['ref']
        commits = payload['pull_request']['commits']
        title = payload['pull_request']['title']
        comments = payload['pull_request']['body']
        repo_full_name = payload['repository']['full_name']
        head_sha = payload['pull_request']['head']['sha']

        log.debug(f'Processing GitHub PR #{number}')

        head_msg = await self._get_commit_msg(repo_full_name, head_sha)
        if allow_skip and self._has_skip(head_msg):
            log.info(f'GitHub PR #{number}, Ignoring: head commit message '
                     f'contains skip pattern')
            return ([], 'git')

        action = payload.get('action')
        if action not in ('opened', 'reopened', 'synchronize'):
            log.info(f'GitHub PR #{number} {action}, ignoring')
            return (changes, 'git')

        properties = self.extractProperties(payload['pull_request'])
        properties.update({'event': event})
        properties.update({'basename': basename})

        plural = 's' if commits != 1 else ''
        desc = f'GitHub Pull Request #{number} ({commits} commit{plural})'
        desc = '\n'.join([desc, title, comments])

        files = await self._get_pull_request_files(repo_full_name, number)

        change = {
            'revision': payload['pull_request']['head']['sha'],
            'when_timestamp': dateparse(payload['pull_request']['created_at']),
            'branch': refname,
            'revlink': payload['pull_request']['_links']['html']['href'],
            'repository': payload['repository']['html_url'],
            'project': payload['pull_request']['base']['repo']['full_name'],
            'category': 'pull',
            # TODO: Get author name based on login id using txgithub module
            'author': payload['sender']['login'],
            'comments': desc,
            'properties': properties,
            'files': files
        }

        if callable(self._codebase):
            change['codebase'] = self._codebase(payload)
        elif self._codebase is not None:
            change['codebase'] = self._codebase

        changes.append(change)
        log.info(f'Received {len(changes)} changes from GitHub PR #{number}')

        return (changes, 'git')

    @ensure_deferred
    async def handle_issue_comment(self, payload, event):
        # no comment handler is configured, so omit issue/pr comments
        if self.comment_handler is None:
            return [], 'git'

        # only allow users of apache org to submit commands, for more see
        # https://developer.github.com/v4/enum/commentauthorassociation/
        allowed_roles = {'OWNER', 'MEMBER', 'CONTRIBUTOR'}

        mention = f'@{self.botname}'
        repo = payload['repository']
        issue = payload['issue']
        comment = payload['comment']

        async def respond(body, preformatted=False):
            if body in {'+1', '-1'}:
                reactions_url = (
                    f"{repo['url']}/issues/comments/{comment['id']}/reactions"
                )
                accept = 'application/vnd.github.squirrel-girl-preview+json'
                return await self._post(reactions_url,
                                        data={'content': body},
                                        headers={'Accept': accept})
            else:
                if preformatted:
                    body = f'```\n{body}\n```'
                return await self._post(issue['comments_url'],
                                        data={'body': body})

        if payload['sender']['login'] == self.botname:
            # don't respond to itself
            return [], 'git'
        elif payload['action'] not in {'created', 'edited'}:
            # don't respond to comment deletion
            return [], 'git'
        elif comment['author_association'] not in allowed_roles:
            # don't respond to comments from non-authorized users
            return [], 'git'
        elif not comment['body'].lstrip().startswith(mention):
            # ursabot is not mentioned, nothing to do
            return [], 'git'
        elif 'pull_request' not in issue:
            await respond('Ursabot only listens to pull request comments!')
            return [], 'git'

        try:
            command = comment['body'].split(mention)[-1].strip()
            properties = self.comment_handler(command)
        except CommandError as e:
            await respond(e.message, preformatted=True)
            return [], 'git'
        except Exception as e:
            log.error(e)
            return [], 'git'
        else:
            if not properties:
                raise ValueError('`comment_parser` must return properties')

        changes = []
        try:
            pull_request = await self._get(issue['pull_request']['url'])
            # handle_pull_request contains pull request specific logic
            changes, _ = await self.handle_pull_request(
                payload={
                    'action': 'synchronize',
                    'sender': payload['sender'],
                    'repository': payload['repository'],
                    'pull_request': pull_request,
                    'number': pull_request['number'],
                },
                event=event,
                allow_skip=False
            )
            # `event: issue_comment` will be available between the properties,
            # but We still need a way to determine which builders to run, so
            # pass the command property as well and flag the change category as
            # `comment` instead of `pull`
            for change in changes:
                change['category'] = 'comment'
                change['properties'].update(properties)
        except Exception as e:
            log.error(e)
            await respond("I've failed to start builds for this PR")
        else:
            n = len(changes)
            log.info(f'Successfully added {n} changes for command {command}')
            if self.use_reactions:
                await respond('+1')
            else:
                await respond("I've successfully started builds for this PR")
        finally:
            return changes, 'git'

    # TODO(kszucs): ursabot might listen on:
    # - handle_commit_comment
    # - handle_pull_request_review
    # - handle_pull_request_review_comment


class UrsabotHook(GithubHook):

    botname = 'ursabot'
    headers = {'User-Agent': 'Ursabot'}
    use_reactions = True
