#!/usr/bin/env python3
"""Publish the checked static site to the owner's GitHub Pages repository.
Uses gh's existing authentication. Never reads or prints its token.
"""
import base64
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import quote
from package_site import public_files, package

ROOT=Path(__file__).resolve().parents[1]
OWNER='sowiloprojectcontact'
REPO=OWNER+'.github.io'
MARKER={'project':'sowilo-site','schema':1}


class GitHub:
    def request(self, endpoint, method='GET', payload=None, missing_ok=False):
        command=['gh','api',endpoint,'--method',method,'--header','Accept: application/vnd.github+json']
        if payload is not None:command+=['--input','-']
        result=subprocess.run(command,input=json.dumps(payload) if payload is not None else None,
                              capture_output=True,text=True,timeout=90)
        if result.returncode:
            if missing_ok and 'HTTP 404' in result.stderr:return None
            raise RuntimeError('GitHub inaccessible ou action refusée. Vérifier la connexion avec gh auth status. '+result.stderr.strip()[:250])
        return json.loads(result.stdout) if result.stdout.strip() else {}


def publish(api=None, attempts=24, pause=time.sleep):
    package()
    api=api or GitHub()
    profile=api.request('user')
    if profile.get('login','').lower()!=OWNER:
        raise RuntimeError('Le compte GitHub connecté doit être '+OWNER+'. Aucun dépôt modifié.')
    endpoint='repos/'+OWNER+'/'+REPO
    metadata=api.request(endpoint,missing_ok=True)
    created=metadata is None
    if created:
        metadata=api.request('user/repos','POST',{'name':REPO,'description':'Sowilo — Community Linux et actualités du projet','private':False,'auto_init':True})
    if metadata.get('private'):
        raise RuntimeError('Le dépôt existant est privé : sa visibilité est conservée ; publication interrompue.')
    branch=metadata['default_branch']
    ref=api.request(endpoint+'/git/ref/heads/'+quote(branch,safe=''))
    parent=ref['object']['sha']
    commit=api.request(endpoint+'/git/commits/'+parent)
    tree=api.request(endpoint+'/git/trees/'+commit['tree']['sha'])
    managed=api.request(endpoint+'/contents/.sowilo-site.json',missing_ok=True)
    if managed:
        try:known=json.loads(base64.b64decode(managed['content']))==MARKER
        except (ValueError,KeyError):known=False
        if not known:raise RuntimeError('Marqueur de site différent : dépôt conservé sans modification.')
    elif not created and {entry['path'] for entry in tree.get('tree',[])}-{'README.md'}:
        raise RuntimeError('Le dépôt contient déjà un autre site. Aucun fichier remplacé.')
    entries=[]
    files={path.relative_to(ROOT).as_posix():path.read_bytes() for path in public_files()}
    for name in ('README.md', '.gitignore', 'scripts/check_site.py', 'scripts/package_site.py', 'scripts/publish_github.py', 'docs/VALIDATION.md'):
        if (ROOT/name).is_file():
            files[name]=(ROOT/name).read_bytes()
    files['.sowilo-site.json']=(json.dumps(MARKER,indent=2)+'\n').encode()
    for relative,content in files.items():
        blob=api.request(endpoint+'/git/blobs','POST',{'encoding':'base64','content':base64.b64encode(content).decode('ascii')})
        entries.append({'path':relative,'mode':'100644','type':'blob','sha':blob['sha']})
    new_tree=api.request(endpoint+'/git/trees','POST',{'base_tree':commit['tree']['sha'],'tree':entries})
    new_commit=api.request(endpoint+'/git/commits','POST',{'message':'Publier la vitrine Community et les actualités Sowilo','tree':new_tree['sha'],'parents':[parent]})
    api.request(endpoint+'/git/refs/heads/'+quote(branch,safe=''),'PATCH',{'sha':new_commit['sha'],'force':False})
    pages=api.request(endpoint+'/pages',missing_ok=True)
    if pages is None:
        pages=api.request(endpoint+'/pages','POST',{'build_type':'legacy','source':{'branch':branch,'path':'/'}})
    elif pages.get('source')!={'branch':branch,'path':'/'} or pages.get('build_type','legacy')!='legacy':
        raise RuntimeError('Sources publiées, mais configuration Pages existante différente : vérifier Settings → Pages sans écrasement automatique.')
    for _ in range(attempts):
        latest=api.request(endpoint+'/pages/builds/latest',missing_ok=True)
        if latest and latest.get('commit')==new_commit['sha']:
            if latest.get('status')=='built':
                pages=api.request(endpoint+'/pages')
                result={'repository':metadata['html_url'],'commit':new_commit['sha'],'url':pages['html_url'],'status':'published'}
                (ROOT/'dist/publication.json').write_text(json.dumps(result,indent=2)+'\n')
                return result
            if latest.get('status')=='errored':raise RuntimeError('Construction Pages en échec ; consulter Actions dans le dépôt.')
        pause(5)
    raise RuntimeError('Sources publiées et Pages configuré. Déploiement encore non confirmé : consulter Settings → Pages et Actions.')


if __name__=='__main__':
    try:
        result=publish()
        print('Publication GitHub Pages vérifiée : '+result['url'])
    except (RuntimeError,ValueError,OSError,subprocess.TimeoutExpired) as error:
        print(str(error),file=sys.stderr)
        raise SystemExit(1)
