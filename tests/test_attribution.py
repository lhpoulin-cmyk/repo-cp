"""Synthetic public attribution contracts; no authenticated operations."""
import copy
from contextlib import ExitStack
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp import attribution as a

FIX = ROOT / 'tests/fixtures/attribution'


def fixture(name='human'):
    return json.loads((FIX / (name + '.json')).read_bytes())


def wire(data):
    return json.dumps(data, ensure_ascii=True).encode()


def result(data):
    output, status = a.report(wire(data))
    return json.loads(output), status


def parts(data):
    parsed = a.parse_record(data['commits'][0])
    return parsed['actors'], parsed['claims'], parsed['models'], parsed['work']


def rewrite(data, actors, claims, models=(), work=None):
    lines = ['Synthetic fixture', '', 'Attribution-Version: 1']
    if work:
        lines.append('Attribution-Work: ' + json.dumps(work))
    for key, items in [('Actor', actors), ('Model', models), ('Claim', claims)]:
        lines.extend('Attribution-' + key + ': ' + json.dumps(item) for item in items)
    data['commits'][0]['message'] = '\n'.join(lines) + '\n'
    return data


def declaration(id, subject, predicate, value, scope=None):
    return {'id': id, 'subject': subject, 'predicate': predicate, 'value': value,
            'scope': scope or {'kind': 'commit', 'target': 'self'},
            'evidence': [{'claim': id, 'state': 'declared', 'by': 'h1', 'method': 'statement-v1',
                          'ref': 'self:trailer/' + id}]}


class AttributionTests(unittest.TestCase):
    def assert_bad(self, raw):
        stdout, stderr = io.StringIO(), io.StringIO()
        status = a.main([], io.BytesIO(raw), stdout, stderr)
        self.assertEqual((status, stdout.getvalue(), stderr.getvalue()), (2, '', a.ERROR))

    def test_human_and_golden(self):
        data, status = result(fixture())
        self.assertEqual(status, 0)
        self.assertEqual(data['totals']['commits']['human-only'], 1)
        self.assertEqual(data['totals']['executor'], {'human': 1})
        self.assertEqual(data['registry']['principals'][0]['source_status'], 'proposed')
        self.assertNotIn('synthetic@example.invalid', a.dumps(data))
        for name in ('human', 'commit-only', 'work-only'):
            raw = (FIX / (name + '.json')).read_bytes()
            self.assertEqual(a.report(raw)[0], (FIX / (name + '.golden.json')).read_text())

    def test_scope_separation_both_directions(self):
        data, _ = result(fixture('commit-only'))
        self.assertEqual(data['totals']['commits']['human-only'], 1)
        self.assertEqual(data['totals']['works']['undetermined'], 1)
        data, _ = result(fixture('work-only'))
        self.assertEqual(data['totals']['commits']['undetermined'], 1)
        self.assertEqual(data['totals']['works']['mixed'], 1)
        self.assertTrue(data['works'][0]['non_additive'])

    def test_negative_unknown_and_conflict(self):
        for present, expected in [(False, 'undetermined'), (None, 'undetermined')]:
            data = fixture(); actors, claims, models, work = parts(data)
            c = claims[0]; c['value']['present'] = present
            if present is None:
                c['evidence'] = [{'claim': c['id'], 'state': 'unknown', 'reason': 'not-recorded'}]
            report, _ = result(rewrite(data, actors, claims))
            self.assertEqual(report['commits'][0]['classification'], expected)
        data = fixture(); actors, claims, _, _ = parts(data)
        claims.append(declaration('deny', 'h1', 'participation', {'role': 'implement', 'present': False}))
        report, status = result(rewrite(data, actors, claims))
        self.assertEqual(status, 2)
        self.assertEqual(report['totals']['record_status'], {'invalid': 1})

    def test_executor_not_author_or_contributor(self):
        data = fixture(); actors, claims, _, _ = parts(data)
        actors.append({'id': 'a1', 'kind': 'agent', 'principal': None, 'tool': 'synthetic', 'models': []})
        claims[-1]['value']['executor'] = 'a1'
        report, _ = result(rewrite(data, actors, claims))
        self.assertEqual(report['commits'][0]['classification'], 'human-only')
        self.assertEqual(report['totals']['executor'], {'agent': 1})
        self.assertEqual(report['commits'][0]['observations'][1]['value']['principal_id'], 'human.example')

    def test_unknown_and_missing_executor(self):
        data = fixture(); actors, claims, _, _ = parts(data)
        c = claims[-1]
        c['value'] = {'executor': None, 'mechanism': None, 'acting_principal': None,
                      'unknown': {k: 'not-recorded' for k in ('executor', 'mechanism', 'acting_principal')}}
        c['evidence'] = [{'claim': c['id'], 'state': 'unknown', 'reason': 'not-recorded'}]
        report, status = result(rewrite(data, actors, claims))
        self.assertEqual(status, 1)
        self.assertEqual(report['totals']['executor'], {'unknown': 1})
        report, status = result(rewrite(data, actors, claims[:-1]))
        self.assertEqual(status, 2)
        self.assertEqual(report['commits'][0]['findings'], ['EXECUTOR_REQUIRED'])

    def test_missing_and_unsupported(self):
        for message, status in [('No metadata', 'missing'), ('Subject\n\nAttribution-Version: 2\n', 'unsupported')]:
            data = fixture(); data['commits'][0]['message'] = message
            report, _ = result(data)
            self.assertEqual(report['commits'][0]['status'], status)
            self.assertEqual(report['totals']['repository_occurrences'], 1)

    def test_model_metadata_and_multiple_models(self):
        data = fixture(); actors, claims, _, _ = parts(data)
        actors.append({'id': 'a1', 'kind': 'agent', 'principal': None, 'tool': 'synthetic', 'models': ['m1', 'm2']})
        model = {'id': 'm1', 'deployment': 'local', 'provider': None, 'model_id': 'synthetic', 'tag': 'demo:1',
                 'resolved_digest': 'sha256:' + 'a' * 64, 'revision': None, 'quantization': 'Q4_K_M',
                 'unavailable': {'provider': 'not-recorded', 'revision': 'not-exposed'}}
        other = dict(model, id='m2', quantization='Q8_0')
        claims.append(declaration('draft', 'a1', 'participation', {'role': 'draft', 'present': True}))
        report, _ = result(rewrite(data, actors, claims, [model, other]))
        self.assertEqual(len(report['commits'][0]['models']), 2)
        self.assertEqual(report['commits'][0]['classification'], 'mixed')
        model['unavailable'] = {}
        self.assertEqual(result(rewrite(data, actors, claims, [model, other]))[1], 2)

    def test_duplicate_rules(self):
        data = fixture(); actors, claims, _, _ = parts(data)
        report, _ = result(rewrite(data, actors + actors, claims + claims))
        self.assertEqual(len(report['commits'][0]['claims']), 3)
        self.assertEqual(len(report['commits'][0]['occurrences']['claim:p1']), 2)
        data['commits'][0]['message'] += 'Attribution-Version: 1\n'
        self.assertEqual(result(data)[1], 2)
        bad = copy.deepcopy(claims[0]); bad['value']['present'] = False
        self.assertEqual(result(rewrite(data, actors, claims + [bad]))[1], 2)

    def test_object_duplicates_and_integration(self):
        data = fixture(); data['commits'][0]['parents'] = ['sha1:' + '3'*40, 'sha1:' + '4'*40]
        data['commits'].append(copy.deepcopy(data['commits'][0]))
        report, _ = result(data)
        self.assertEqual(report['totals']['unique_objects'], 1)
        self.assertEqual(report['totals']['integration_commits'], 1)
        self.assertEqual(report['commits'][0]['input_occurrences'], [0, 1])
        data['commits'][1]['message'] += 'bad'
        report, status = result(data)
        self.assertEqual(status, 2)
        self.assertEqual(report['commits'][0]['findings'], ['OBJECT_CONFLICT'])

    def test_registry_ambiguity_and_second_human(self):
        data = fixture(); b = copy.deepcopy(data['registry']['git_identity_bindings'][0]); b['id'] = 'other'
        data['registry']['git_identity_bindings'].append(b)
        report, status = result(data)
        self.assertEqual(status, 1)
        self.assertEqual(report['commits'][0]['observations'][0]['value']['status'], 'UNKNOWN')
        data = fixture(); actors, claims, _, _ = parts(data)
        actors.append({'id':'h2','kind':'human','principal':'human.second','tool':None,'models':[]})
        claims.append(declaration('review', 'h2', 'participation', {'role':'review','present':True}))
        report, _ = result(rewrite(data, actors, claims))
        self.assertEqual(report['commits'][0]['exclusive'], 'shared')

    def test_binding_aliases_and_repeated_work(self):
        data = fixture('commit-only'); actors, claims, _, work = parts(data)
        for c in claims[:2]:
            c['scope'] = {'kind':'work','target':work}
        claims.append(declaration('binding','h1','identity-binding',{'registry_revision':data['registry']['source_revision'],'binding_id':'git.example'}))
        rewrite(data, actors, claims, work=work)
        data['commits'].append(dict(data['commits'][0],oid='sha1:'+'3'*40))
        report, _ = result(data)
        self.assertEqual(report['works'][0]['exclusive'], 'exclusive')
        self.assertEqual(len(report['works'][0]['participation']), 1)
        self.assertEqual(len(report['works'][0]['sources']), 2)
        work2 = copy.deepcopy(work); work2['revision'] = 'sha1:'+'5'*40
        data['commits'][1]['message'] = data['commits'][1]['message'].replace(work['revision'],work2['revision'])
        report, _ = result(data)
        self.assertEqual(report['totals']['work_scopes'], 2)
        self.assertEqual(report['totals']['work_entries'], 1)

    def test_observation_time_no_clock_environment_or_runtime_io(self):
        raw = wire(fixture())
        first = a.report(raw)
        with ExitStack() as stack:
            for target in ('builtins.open','pathlib.Path.open','subprocess.run','subprocess.Popen',
                           'socket.socket','os.getenv','time.time','os.open'):
                stack.enter_context(patch(target, side_effect=AssertionError(target)))
            self.assertEqual(first, a.report(raw))
        data = fixture(); data['captured_at'] = '2026-10-02T00:00:00Z'
        report, _ = result(data)
        self.assertTrue(all(o['at'] == data['captured_at'] for o in report['commits'][0]['observations']))
        data['captured_at'] = '2026-02-30T00:00:00Z'
        self.assert_bad(wire(data))

    def test_profile_mismatch_and_unknown(self):
        data = fixture(); check = fixture('profiles');data['profile_checks']=[check]
        self.assertEqual(result(data)[1], 0)
        check['observed']['push_destinations']=['https://example.invalid/wrong.git']
        report, status = result(data)
        self.assertEqual(status, 2)
        self.assertEqual(report['profile_checks'][0]['findings'], ['PROFILE_MISMATCH'])
        check['observed']=copy.deepcopy(check['expected']);check['observed']['transport_account_ref']=None
        self.assertEqual(result(data)[1], 1)

    def test_bad_outer_json(self):
        for raw in [b'{',b'\xff',b'\xef\xbb\xbf{}',b'NaN',b'Infinity',b'1.0',b'{"x":1,"x":2}',
                    b'{"n":{"x":1,"x":2}}',b'['*2000,b'9'*10000,b'9223372036854775808',
                    br'"\ud800"',br'"\udfff"',br'"\ud800X"',br'"\udc00\ud800"',
                    br'"\uZZZZ"',b'"\xed\xa0\x80"',b'x'*(a.MAX_INPUT+1)]:
            with self.subTest(raw_length=len(raw)):
                self.assert_bad(raw)
        self.assertEqual(a.load(br'"\ud83d\ude00"'), '\U0001f600')
        with self.assertRaises(a.Invalid):
            a.load('\ud800')

    def test_bad_nested_trailer_json(self):
        for bad in ['{"id":1,"id":2}', '{"id":"\\ud800"}', '{"id":"\\udfff"}',
                    '{"id":"\\ud800X"}', '{"id":'+'9'*10000+'}', '{"id":1.5}', '{"id":NaN}', '{']:
            data = fixture();data['commits'][0]['message'] += 'Attribution-Claim: '+bad+'\n'
            report, status = result(data)
            self.assertEqual(status, 2)
            self.assertEqual(report['commits'][0]['claims'], [])
            self.assertNotIn('Traceback', a.dumps(report))

    def test_non_bmp_is_valid_but_controls_are_not(self):
        data=fixture();actors,claims,_,_=parts(data)
        claims[-1]['evidence'][0]['ref']='public:\U0001f600'
        self.assertEqual(result(rewrite(data,actors,claims))[1],0)
        for value in ['\ud800','\udfff','\x00','\x1b','\u202e','\u2066']:
            data=fixture();data['registry']['principals'][0]['source_status']=value
            self.assert_bad(wire(data))

    def test_semantic_validation(self):
        mutations=[lambda c:c.update(extra=True),lambda c:c['evidence'][0].pop('method'),
                   lambda c:c['evidence'][0].pop('ref'),lambda c:c['evidence'][0].update(claim='wrong'),
                   lambda c:c['evidence'][0].update(by='missing'),lambda c:c.update(subject='missing')]
        for mutate in mutations:
            data=fixture();actors,claims,_,_=parts(data);mutate(claims[0])
            self.assertEqual(result(rewrite(data,actors,claims))[1],2)
        for state in ('observed','verified'):
            data=fixture();actors,claims,_,_=parts(data);claims[0]['evidence'][0]['state']=state
            report,status=result(rewrite(data,actors,claims))
            self.assertEqual(status,2)
            self.assertEqual(report['commits'][0]['findings'],['UNSUPPORTED_EVIDENCE_STATE'])

    def test_grammar_failures(self):
        data=fixture();message=data['commits'][0]['message']
        for bad in [message.replace('Attribution-Version: 1\n',''),message+'Attribution-New: x\n',
                    'Attribution-Version: 1\n\n'+message, message+' continuation\n',
                    message.replace('\n\n','\n',1)]:
            data['commits'][0]['message']=bad
            self.assertEqual(result(data)[1],2)

    def test_provenance_authorization_and_signature_no_promotion(self):
        data=fixture();actors,claims,_,_=parts(data)
        for n,relation in enumerate(['rebased-from','cherry-picked-from','squashed-from','copied-from','merged-from']):
            claims.append(declaration('source'+str(n),'record','provenance',{'relation':relation,'source':{'repository':{'id':'repo.source'},'oid':'sha1:'+'6'*40}}))
        claims.append(declaration('sig','record','signature',{'signer_reference':'synthetic.signer','valid':True}))
        report,status=result(rewrite(data,actors,claims))
        self.assertEqual(status,0)
        self.assertEqual(len([c for c in report['commits'][0]['claims'] if c['predicate']=='provenance']),5)
        self.assertTrue(all(e['state'] != 'verified' for c in report['commits'][0]['claims'] for e in c['evidence']))
        claims.append(declaration('approval','h1','authorization',{'decision':'approved','action':'publish'}))
        self.assertEqual(result(rewrite(data,actors,claims))[1],2)

    def test_bounds(self):
        data=fixture();data['commits']*=1001;self.assert_bad(wire(data))
        data=fixture();data['commits'][0]['message']='x'*131073;self.assert_bad(wire(data))
        for field in ('name','email'):
            data=fixture();data['commits'][0]['author'][field]='x'*2049;self.assert_bad(wire(data))
        data=fixture();actors,claims,_,_=parts(data)
        for n in range(129):
            claims.append(declaration('extra'+str(n),'h1','participation',{'role':'review','present':True}))
        self.assertEqual(result(rewrite(data,actors,claims))[1],2)
        data=fixture();actors,claims,_,_=parts(data);claims[0]['evidence']*=9
        self.assertEqual(result(rewrite(data,actors,claims))[1],2)

    def test_secret_indicator_not_echoed(self):
        data=fixture();data['commits'][0]['message']='token='+'SYNTHETIC'*5
        self.assert_bad(wire(data))

    def test_cli_safe_errors_and_no_partial_output(self):
        for raw in [b'{',b'9'*10000,br'"\ud800"',wire(fixture())]:
            p=subprocess.run([sys.executable,'-B',str(ROOT/'tools/repo-cp'),'attribution-report'],
                             input=raw,capture_output=True,env={'PATH':'/usr/bin:/bin','PYTHONDONTWRITEBYTECODE':'1'})
            if raw==wire(fixture()):
                self.assertEqual(p.returncode,0)
                self.assertEqual(p.stderr,b'')
            else:
                self.assertEqual((p.returncode,p.stdout,p.stderr),(2,b'',a.ERROR.encode()))

    def test_invalid_source_preserves_safe_work_exclusion(self):
        data=fixture('commit-only')
        data['commits'][0]['message'] += 'Attribution-Claim: {\n'
        report,status=result(data)
        self.assertEqual(status,2)
        self.assertEqual(report['works'][0]['excluded_sources'],1)
        self.assertEqual(report['works'][0]['classification'],'undetermined')
        self.assertEqual(report['commits'][0]['claims'],[])

    def test_work_conflict_visible_without_commit_scope_promotion(self):
        data=fixture('commit-only');actors,claims,_,work=parts(data)
        claims.append(declaration('bind','h1','identity-binding',{'registry_revision':data['registry']['source_revision'],'binding_id':'git.example'}))
        claims.append(declaration('wp','h1','participation',{'role':'design','present':True},{'kind':'work','target':work}))
        rewrite(data,actors,claims,work=work)
        second=copy.deepcopy(data['commits'][0]);second['oid']='sha1:'+'3'*40
        other=copy.deepcopy(data);other['commits']=[second]
        a2,c2,_,w2=parts(other);c2[-1]['value']['present']=False
        rewrite(other,a2,c2,work=w2);data['commits'].append(other['commits'][0])
        report,status=result(data)
        self.assertEqual(status,2)
        self.assertEqual(report['totals']['commits']['human-only'],2)
        self.assertEqual(report['works'][0]['classification'],'unclassifiable')
        self.assertEqual(len(report['works'][0]['claims']),2)

    def test_explicit_commit_target_only_counts_for_target(self):
        data=fixture();actors,claims,_,_=parts(data)
        target={'repository':{'id':'repo.example'},'oid':'sha1:'+'3'*40}
        claims[0]['scope']={'kind':'commit','target':target}
        claims[1]['scope']={'kind':'commit','target':target}
        rewrite(data,actors,claims)
        data['commits'].append(dict(data['commits'][0],oid=target['oid'],message='No trailers'))
        report,_=result(data)
        self.assertEqual(report['commits'][0]['classification'],'undetermined')
        self.assertEqual(report['commits'][1]['classification'],'human-only')
        self.assertEqual(report['commits'][1]['status'],'missing')

    def test_distinct_assertion_ids_do_not_double_count(self):
        data=fixture();actors,claims,_,_=parts(data)
        claims.append(declaration('same-role','h1','participation',{'role':'implement','present':True}))
        report,_=result(rewrite(data,actors,claims))
        views=report['totals']['commit_participation_views']
        self.assertEqual(views['kinds'],{'human':1})
        self.assertEqual(views['roles'],{'implement':1})
        self.assertEqual(list(views['actors'].values()),[1])
        self.assertTrue(views['non_additive'])

    def test_remaining_predicates_and_unknown_reasons(self):
        data=fixture();actors,claims,_,work=parts(fixture('commit-only'))
        extras=[declaration('responsible','h1','responsibility','accepted'),
                declaration('descriptor','h1','descriptor-field',{'pointer':'/kind','expected':'human'}),
                declaration('header','record','git-header',{'field':'author','name':'Synthetic','email':'public@example.invalid'}),
                declaration('auth','h1','authorization',{'decision':'approved','action':'review'},{'kind':'work','target':work})]
        self.assertEqual(result(rewrite(data,actors,claims+extras))[0]['commits'][0]['status'],'valid')
        cases=[('responsibility',None,'h1'),('identity-binding',None,'h1'),
               ('authorization',{'decision':None,'action':'review'},'h1'),
               ('provenance',{'relation':'copied-from','source':None},'record'),
               ('signature',{'signer_reference':None,'valid':None},'record')]
        for predicate,value,subject in cases:
            c=declaration('unknown',subject,predicate,value,{'kind':'work','target':work} if predicate=='authorization' else None)
            c['evidence']=[{'claim':'unknown','state':'unknown','reason':'not-recorded'}]
            report,status=result(rewrite(data,actors,claims+[c]))
            self.assertEqual(status,1)
            self.assertEqual(report['commits'][0]['status'],'valid')

    def test_more_exact_bounds(self):
        data=fixture();actors,claims,_,_=parts(data)
        for n in range(32):
            actors.append({'id':'human'+str(n),'kind':'human','principal':None,'tool':None,'models':[]})
        self.assertEqual(result(rewrite(data,actors,claims))[1],2)
        data=fixture();actors,claims,_,_=parts(data);actors[0]['id']='x'*129
        self.assertEqual(result(rewrite(data,actors,claims))[1],2)
        data=fixture();actors,claims,_,_=parts(data)
        for n in range(4):
            claims[0]['evidence'].append(dict(claims[0]['evidence'][0],ref='x'*2048))
        self.assertEqual(result(rewrite(data,actors,claims))[1],2)
        self.assertEqual(a.load(b'9223372036854775807'),2**63-1)
        self.assert_bad(b'-9223372036854775809')
        for n in (20,128,4097):
            data=fixture();data['commits'][0]['message']+='Attribution-Claim: {"value":'+('9'*n)+'}\n'
            self.assertEqual(result(data)[1],2)

    def test_utf8_size_not_character_count(self):
        data=fixture();data['commits'][0]['message']='\U0001f600'*40000
        report,status=result(data)
        self.assertEqual(status,2)
        self.assertEqual(report['commits'][0]['status'],'invalid')

    def test_model_union_for_repeated_normalized_work_actor(self):
        data=fixture('work-only');actors,claims,_,work=parts(data)
        # A declared agent principal uses the same generic projection structure.
        data['registry']['principals'].append({'id':'agent.synthetic','kind':'agent','source_status':'unverified'})
        data['registry']['git_identity_bindings'].append({'id':'git.agent','principal_id':'agent.synthetic',
            'name':'Synthetic Agent','email':'agent@example.invalid','repository_ids':['repo.example'],'source_status':'unverified'})
        model={'id':'m1','deployment':'local','provider':None,'model_id':'synthetic','tag':'test:1',
               'resolved_digest':None,'revision':None,'quantization':'Q4',
               'unavailable':{'provider':'not-recorded','resolved_digest':'not-recorded','revision':'not-recorded'}}
        actors[1]['principal']='agent.synthetic';actors[1]['models']=['m1']
        claims.append(declaration('binding-agent','a1','identity-binding',
            {'registry_revision':data['registry']['source_revision'],'binding_id':'git.agent'}))
        rewrite(data,actors,claims,[model],work)
        data['commits'].append(dict(data['commits'][0],oid='sha1:'+'3'*40))
        report,_=result(data)
        participant=next(p for p in report['works'][0]['participation'] if p['kind']=='agent')
        self.assertEqual(len(participant['models']),2)
        self.assertEqual(len(report['totals']['work_participation_views']['models']),2)

    def test_agent_only_and_multiple_authorization_actions(self):
        data=fixture();actors,claims,_,_=parts(data)
        actors.append({'id':'a1','kind':'agent','principal':None,'tool':'synthetic','models':[]})
        claims[0]['subject']='a1'
        report,_=result(rewrite(data,actors,claims))
        self.assertEqual(report['commits'][0]['classification'],'agent-only')
        target={'kind':'commit','target':{'repository':{'id':'repo.example'},'oid':'sha1:'+'3'*40}}
        for action in ('review','publish'):
            claims.append(declaration('action-'+action,'h1','authorization',{'decision':'approved','action':action},target))
        self.assertEqual(result(rewrite(data,actors,claims))[0]['commits'][0]['status'],'valid')

    def test_cross_record_commit_conflict_excludes_sources_from_work(self):
        data=fixture('commit-only');actors,claims,_,work=parts(data)
        claims.append(declaration('bind','h1','identity-binding',
            {'registry_revision':data['registry']['source_revision'],'binding_id':'git.example'}))
        claims.append(declaration('work-positive','h1','participation',{'role':'review','present':True},{'kind':'work','target':work}))
        rewrite(data,actors,claims,work=work)
        other=copy.deepcopy(data);other['commits'][0]['oid']='sha1:'+'3'*40
        actors2,claims2,_,_=parts(other)
        claims2[0]['value']['present']=False
        claims2[0]['scope']={'kind':'commit','target':{'repository':{'id':'repo.example'},'oid':data['commits'][0]['oid']}}
        rewrite(other,actors2,claims2,work=work)
        data['commits'].append(other['commits'][0])
        report,status=result(data)
        self.assertEqual(status,2)
        self.assertEqual(report['totals']['record_status'],{'invalid':2})
        self.assertEqual(report['works'][0]['participation'],[])
        self.assertEqual(report['works'][0]['excluded_sources'],2)

    def test_whitespace_body_is_bounded_missing_input(self):
        data=fixture();data['commits'][0]['message']='\n'*100000
        report,status=result(data)
        self.assertEqual(status,1)
        self.assertEqual(report['commits'][0]['status'],'missing')
