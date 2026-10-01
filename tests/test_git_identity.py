"""Git is permitted only in this isolated synthetic development harness."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp.attribution import check_profile, report


class GitIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='repocp-identity-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.hooks = self.root/'empty-hooks'; self.hooks.mkdir()
        self.config = self.root/'global.gitconfig'
        # Explicit allowlist, never copy os.environ, live homes, SSH or CLI state.
        self.env = {'PATH':'/usr/bin:/bin', 'LANG':'C', 'LC_ALL':'C',
                    'GIT_CONFIG_NOSYSTEM':'1', 'GIT_CONFIG_SYSTEM':'/dev/null',
                    'GIT_CONFIG_GLOBAL':str(self.config), 'GIT_TERMINAL_PROMPT':'0',
                    'GIT_ALLOW_PROTOCOL':'file', 'GIT_AUTHOR_DATE':'2000-01-01T00:00:00Z',
                    'GIT_COMMITTER_DATE':'2000-01-01T00:00:00Z', 'PYTHONDONTWRITEBYTECODE':'1'}
        self.config.write_text('[user]\n useConfigOnly = true\n[commit]\n gpgSign = false\n'
                               '[core]\n hooksPath = '+str(self.hooks)+'\n[credential]\n helper =\n')
        for profile in ('a','b'):
            folder = self.root/profile; folder.mkdir()
            inc = self.root/(profile+'.inc')
            inc.write_text('[user]\n name = Synthetic Human\n email = '+profile+'@example.invalid\n'
                           '[helix]\n identityProfile = '+profile+'\n')
            with self.config.open('a') as stream:
                stream.write('[includeIf "gitdir:'+str(folder)+'/"]\n path = '+str(inc)+'\n')
            repo = folder/'repo'
            self.git(self.root, 'init', '--quiet', '--initial-branch=main', str(repo))
        self.a, self.b = self.root/'a/repo', self.root/'b/repo'

    def git(self, repo, *args, check=True):
        return subprocess.run(['git','-C',str(repo),*args],env=self.env,
                              capture_output=True,text=True,check=check)

    def profile(self, repo):
        def config(k):
            p = self.git(repo,'config','--get',k,check=False)
            return p.stdout.strip() if p.returncode == 0 else None
        identity = {'name':config('user.name'),'email':config('user.email')}
        return {'profile_id':config('helix.identityProfile'),'author':identity,
                'committer':identity,'fetch_destinations':[], 'push_destinations':[],
                'transport_account_ref':'synthetic.none','signing_key_ref':'synthetic.none'}

    def test_profiles_and_disposable_commits(self):
        for repo,label in ((self.a,'a'),(self.b,'b')):
            self.assertEqual(self.profile(repo)['author']['email'],label+'@example.invalid')
            self.git(repo,'commit','--quiet','--allow-empty','-m','Synthetic only')
            headers=self.git(repo,'show','-s','--format=%an|%ae|%cn|%ce','HEAD').stdout.strip()
            self.assertEqual(headers,'Synthetic Human|'+label+'@example.invalid|Synthetic Human|'+label+'@example.invalid')
            self.assertEqual(self.git(repo,'remote').stdout,'')

    def test_wrong_profile_stops_before_commit_or_publication(self):
        expected=self.profile(self.a)
        self.git(self.a,'config','user.email','b@example.invalid')
        check={'id':'wrong','repository_id':'repo.synthetic','expected':expected,'observed':self.profile(self.a)}
        outcome=check_profile(check)
        effects=[]
        if outcome['status']=='MATCH':
            effects.append('commit')
            self.git(self.a,'commit','--allow-empty','-m','Should never happen')
        self.assertEqual(outcome['status'],'MISMATCH')
        self.assertEqual(outcome['findings'],['PROFILE_MISMATCH'])
        self.assertEqual(effects,[])
        self.assertNotEqual(self.git(self.a,'rev-parse','--verify','HEAD',check=False).returncode,0)
        self.assertFalse((self.a/'.git/refs/heads/main').exists())

    def test_wrong_destination_and_unknown_transport(self):
        expected=self.profile(self.a); expected['push_destinations']=['https://example.invalid/a.git']
        observed=copy.deepcopy(expected);observed['push_destinations']=['https://example.invalid/b.git']
        check={'id':'destination','repository_id':'repo.synthetic','expected':expected,'observed':observed}
        self.assertEqual(check_profile(check)['status'],'MISMATCH')
        observed['push_destinations']=expected['push_destinations'];observed['transport_account_ref']=None
        self.assertEqual(check_profile(check)['status'],'UNKNOWN')

    def test_unprofiled_repo_cannot_guess_identity(self):
        repo=self.root/'unprofiled';self.git(self.root,'init','--quiet',str(repo))
        p=self.git(repo,'commit','--allow-empty','-m','No identity',check=False)
        self.assertNotEqual(p.returncode,0)
        self.assertNotEqual(self.git(repo,'rev-parse','--verify','HEAD',check=False).returncode,0)

    def test_independent_repositories_and_linked_worktree(self):
        self.git(self.a,'commit','--quiet','--allow-empty','-m','Synthetic base')
        linked=self.root/'b/linked'
        self.git(self.a,'worktree','add','--quiet','-b','synthetic-linked',str(linked))
        self.git(linked,'config','user.email','shared@example.invalid')
        self.assertEqual(self.profile(self.a)['author']['email'],'shared@example.invalid')
        self.assertEqual(self.profile(self.b)['author']['email'],'b@example.invalid')
        self.assertEqual(self.profile(linked)['profile_id'],'a')

    def test_command_and_environment_overrides_are_visible(self):
        p=self.git(self.a,'-c','user.email=override@example.invalid','var','GIT_AUTHOR_IDENT')
        self.assertIn('<override@example.invalid>',p.stdout)
        self.env['GIT_AUTHOR_EMAIL']='environment@example.invalid'
        self.assertIn('<environment@example.invalid>',self.git(self.a,'var','GIT_AUTHOR_IDENT').stdout)
        self.assertEqual(self.profile(self.a)['author']['email'],'a@example.invalid')

    def test_report_bytes_across_environment_clock_and_directory(self):
        raw=(ROOT/'tests/fixtures/attribution/human.json').read_bytes()
        expected=report(raw)[0].encode()
        for folder,locale in ((self.a,'C'),(self.b,'C.UTF-8')):
            environment=dict(self.env,LC_ALL=locale,TZ='Pacific/Honolulu')
            p=subprocess.run([sys.executable,'-B',str(ROOT/'tools/repo-cp'),'attribution-report'],
                             input=raw,capture_output=True,cwd=folder,env=environment,check=True)
            self.assertEqual(p.stdout,expected)
            self.assertEqual(p.stderr,b'')
